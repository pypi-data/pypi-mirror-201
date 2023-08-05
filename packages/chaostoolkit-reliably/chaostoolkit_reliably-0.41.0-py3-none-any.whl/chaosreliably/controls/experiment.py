import io
import json
import os
import secrets
import threading
import time
from copy import deepcopy
from datetime import datetime, timezone
from logging import Formatter, StreamHandler
from typing import Any, Dict, Optional, cast

from chaoslib.exit import exit_gracefully, exit_ungracefully
from chaoslib.run import EventHandlerRegistry, RunEventHandler
from chaoslib.types import (
    Activity,
    Configuration,
    Experiment,
    Journal,
    Run,
    Schedule,
    Secrets,
    Settings,
)
from logzero import logger

from chaosreliably import RELIABLY_HOST, get_session
from chaosreliably.activities.pauses import reset as reset_activity_pause
from chaosreliably.controls import global_lock

__all__ = ["configure_control"]


class ReliablyHandler(RunEventHandler):  # type: ignore
    def __init__(
        self,
        org_id: str,
        exp_id: str,
        experiment: Experiment,
    ) -> None:
        RunEventHandler.__init__(self)
        self.org_id = org_id
        self.exp_id = exp_id
        self.exec_id = None  # type: Optional[str]
        self.started = datetime.utcnow().replace(tzinfo=timezone.utc)
        self.experiment = deepcopy(experiment)
        self.journal = None  # type: Journal
        self.current_activities = []  # type: ignore

        self.should_stop = threading.Event()
        self.should_pause = threading.Event()
        self.check_lock = threading.Lock()
        self.pause_duration = 0
        self.paused_by_user = ""
        self.paused_by_user_id = ""
        self.paused = False
        self.check_for_user_state = None  # type: Optional[threading.Thread]

        self.stream = io.StringIO()
        self.log_handler = StreamHandler(stream=self.stream)
        self.log_handler.setFormatter(
            Formatter("[%(asctime)s] - %(levelname)s - %(message)s")
        )

        logger.addHandler(self.log_handler)

    def _check(
        self,
        org_id: str,
        exp_id: str,
        exec_id: str,
        configuration: Configuration,
        secrets: Secrets,
    ) -> None:
        logger.debug("Starting Reliably state checker now")

        url = f"/{org_id}/experiments/{exp_id}/executions/{exec_id}/state"
        while not self.should_stop.is_set():
            with get_session(configuration, secrets) as session:
                r = session.get(url)
                if r.status_code > 399:
                    logger.debug(f"Failed to retrieve state: {r.json()}")
                    continue

            state = r.json()
            if state:
                if state["current"] == "terminate":
                    user = state.get("user", {})
                    username = user.get("name", "")
                    self.paused_by_user = ""
                    self.paused_by_user_id = ""

                    logger.info(
                        "Execution state was changed to `terminate` "
                        f"by {username}. "
                        "Exiting now..."
                    )

                    reset_activity_pause()

                    self.extension["termination"] = {
                        "timestamp": datetime.utcnow()
                        .replace(tzinfo=timezone.utc)
                        .isoformat(),
                        "skip_rollbacks": state["skip_rollbacks"],
                    }

                    if state["skip_rollbacks"]:
                        exit_ungracefully()
                    else:
                        exit_gracefully()
                elif state["current"] == "pause":
                    duration = state["duration"]
                    with self.check_lock:
                        if not self.paused:
                            user = state.get("user", {})
                            self.paused_by_user = user.get("name", "")
                            self.paused_by_user_id = user.get("id", "")

                            m = (
                                "Execution state was changed to `pause`. "
                                "Pausing the execution of the current "
                                "activity"
                            )
                            if self.paused_by_user:
                                m = f"{m}, requested by {self.paused_by_user},"

                            if duration:
                                m = f"{m} for {duration}s"
                            else:
                                m = f"{m} indefinitely"
                            m = f"{m} or until state changes back to `resume`"
                            logger.info(m)
                            self.paused = True
                            self.pause_duration = state["duration"]
                            self.should_pause.set()
                elif state["current"] == "resume":
                    reset_activity_pause()

                    with self.check_lock:
                        if self.paused:
                            user = state.get("user", {})
                            username = user.get("name", "")
                            self.paused_by_user = ""
                            self.paused_by_user_id = ""

                            logger.info(
                                "Execution state was changed to `resume` "
                                f"by {username}"
                            )

            now = time.time()
            later = now + 10
            while time.time() < later:
                time.sleep(0.5)
                if self.should_stop.is_set():
                    logger.debug("Stopping Reliably state checker now")
                    break

    def running(
        self,
        experiment: Experiment,
        journal: Journal,
        configuration: Configuration,
        secrets: Secrets,
        schedule: Schedule,
        settings: Settings,
    ) -> None:
        self.experiment = experiment
        self.configuration = configuration
        self.secrets = secrets
        self.journal = journal

        try:
            result = create_run(
                self.org_id,
                self.exp_id,
                experiment,
                journal,
                self.configuration,
                self.secrets,
            )

            if result:
                payload = result
                self.extension = get_reliably_extension_from_journal(journal)

                self.exec_id = payload["id"]
                logger.info(f"Reliably execution: {self.exec_id}")

                host = self.secrets.get(
                    "host", os.getenv("RELIABLY_HOST", RELIABLY_HOST)
                )

                url = f"https://{host}/executions/view/?id={self.exec_id}&exp={self.exp_id}"  # noqa
                self.extension["execution_url"] = url

                add_runtime_extra(self.extension)
                set_plan_status(
                    self.org_id,
                    "running",
                    None,
                    self.configuration,
                    self.secrets,
                )

                set_execution_state(
                    self.org_id,
                    self.exp_id,
                    self.exec_id,
                    {
                        "current": "running",
                        "started_on": self.started.isoformat(),
                    },
                    self.configuration,
                    self.secrets,
                )

                self.check_for_user_state = threading.Thread(
                    None,
                    self._check,
                    args=(
                        self.org_id,
                        self.exp_id,
                        self.exec_id,
                        configuration,
                        secrets,
                    ),
                )
                self.check_for_user_state.start()
        except Exception as ex:
            set_plan_status(
                self.org_id, "error", str(ex), self.configuration, self.secrets
            )

    def finish(self, journal: Journal) -> None:
        logger.info("Finishing Reliably execution...")
        self.should_stop.set()
        if self.check_for_user_state:
            self.check_for_user_state.join(timeout=3)
            self.check_for_user_state = None

        logger.removeHandler(self.log_handler)
        self.log_handler.flush()

        log = self.stream.getvalue()
        self.stream.close()

        self.current_activities = []

        try:
            complete_run(
                self.org_id,
                self.exp_id,
                self.exec_id,
                journal,
                log,
                self.configuration,
                self.secrets,
            )
            set_plan_status(
                self.org_id,
                "completed",
                None,
                self.configuration,
                self.secrets,
            )
        except Exception as ex:
            set_plan_status(
                self.org_id, "error", str(ex), self.configuration, self.secrets
            )
        finally:
            set_execution_state(
                self.org_id,
                self.exp_id,
                self.exec_id,
                {
                    "current": "finished",
                    "status": journal.get("status"),
                    "deviated": journal.get("deviated"),
                },
                self.configuration,
                self.secrets,
            )

            self.experiment = (
                self.configuration
            ) = self.secrets = self.journal = None

        logger.info("Finished Reliably execution. Bye!")

    def start_hypothesis_before(self, experiment: Experiment) -> None:
        with self.check_lock:
            self.current_activities = experiment.get(
                "steady-state-hypothesis", {}
            ).get("probes", [])

    def start_hypothesis_after(self, experiment: Experiment) -> None:
        ssh = experiment.get("steady-state-hypothesis")
        if ssh:
            with self.check_lock:
                self.current_activities = ssh.get("probes", [])
                experiment["steady-state-hypothesis"][
                    "probes"
                ] = self.current_activities

    def start_method(self, experiment: Experiment) -> None:
        with self.check_lock:
            self.current_activities = experiment.get("method", [])

    def start_rollbacks(self, experiment: Experiment) -> None:
        with self.check_lock:
            self.current_activities = experiment.get("rollbacks", [])

    def start_activity(self, activity: Activity) -> None:
        name = activity.get("name")

        with self.check_lock:
            if self.paused:
                pause = {
                    "before_activity": name,
                    "start": datetime.utcnow()
                    .replace(tzinfo=timezone.utc)
                    .isoformat(),
                    "duration": self.pause_duration,
                }
                self.extension["pauses"].append(pause)

        send_journal(
            self.org_id,
            self.exp_id,
            self.exec_id,
            self.journal,
            self.configuration,
            self.secrets,
        )

    def activity_completed(self, activity: Activity, run: Run) -> None:
        name = activity.get("name")

        if self.should_pause.is_set():
            self.should_pause.clear()

            logger.info(f"Adding a pause activity after '{name}'")

            duration = 0
            with self.check_lock:
                duration = self.pause_duration

            index = self.current_activities.index(activity)
            with self.check_lock:
                self.current_activities.insert(
                    index + 1,
                    make_user_pause(
                        duration, self.paused_by_user, self.paused_by_user_id
                    ),
                )
        else:
            with self.check_lock:
                if self.paused:
                    self.paused = False

                    self.extension["pauses"][-1]["end"] = (
                        datetime.utcnow()
                        .replace(tzinfo=timezone.utc)
                        .isoformat()
                    )

                    set_execution_state(
                        self.org_id,
                        self.exp_id,
                        self.exec_id,
                        {
                            "current": "running",
                            "started_on": self.started.isoformat(),
                        },
                        self.configuration,
                        self.secrets,
                    )

                    logger.info("No longer paused")

        send_journal(
            self.org_id,
            self.exp_id,
            self.exec_id,
            self.journal,
            self.configuration,
            self.secrets,
        )


def configure_control(
    experiment: Experiment,
    event_registry: EventHandlerRegistry,
    exp_id: str,
    org_id: str,
    configuration: Configuration = None,
    secrets: Secrets = None,
    **kwargs: Any,
) -> None:
    logger.debug("Configure Reliably's experiment control")
    event_registry.register(ReliablyHandler(org_id, exp_id, experiment))


###############################################################################
# Private functions
###############################################################################
def make_user_pause(
    pause_duration: int = 0, username: str = "", user_id: str = ""
) -> Activity:
    return {
        "type": "action",
        "name": f"reliably-pause-{secrets.token_hex(4)}",
        "provider": {
            "type": "python",
            "module": "chaosreliably.activities.pauses",
            "func": "pause_execution",
            "arguments": {
                "duration": pause_duration,
                "username": username,
                "user_id": user_id,
            },
        },
    }


def create_run(
    org_id: str,
    exp_id: str,
    experiment: Experiment,
    state: Journal,
    configuration: Configuration,
    secrets: Secrets,
) -> Optional[Dict[str, Any]]:
    with get_session(configuration, secrets) as session:
        resp = session.post(
            f"/{org_id}/experiments/{exp_id}/executions",
            json={"result": json.dumps(state)},
        )
        if resp.status_code == 201:
            return cast(Dict[str, Any], resp.json())
    return None


def complete_run(
    org_id: str,
    exp_id: str,
    execution_id: Optional[str],
    state: Journal,
    log: str,
    configuration: Configuration,
    secrets: Secrets,
) -> Optional[Dict[str, Any]]:
    with get_session(configuration, secrets) as session:
        resp = session.put(
            f"/{org_id}/experiments/{exp_id}/executions/{execution_id}/results",
            json={"result": json.dumps(state), "log": log},
        )
        if resp.status_code != 200:
            logger.error("Failed to update results on server")
    return None


def send_journal(
    org_id: str,
    exp_id: str,
    execution_id: Optional[str],
    state: Journal,
    configuration: Configuration,
    secrets: Secrets,
) -> Optional[Dict[str, Any]]:
    with get_session(configuration, secrets) as session:
        resp = session.put(
            f"/{org_id}/experiments/{exp_id}/executions/{execution_id}/results",
            json={"result": json.dumps(state)},
        )
        if resp.status_code != 200:
            logger.error("Failed to update results on server")
    return None


def get_reliably_extension_from_journal(journal: Journal) -> Dict[str, Any]:
    with global_lock:
        experiment = journal.get("experiment")
        extensions = experiment.setdefault("extensions", [])
        for extension in extensions:
            if extension["name"] == "reliably":
                extension.setdefault("pauses", [])
                extension.setdefault("termination", None)
                return cast(Dict[str, Any], extension)

        extension = {"name": "reliably", "pauses": [], "termination": None}
        extensions.append(extension)
        return cast(Dict[str, Any], extension)


def add_runtime_extra(extension: Dict[str, Any]) -> None:
    extra = os.getenv("RELIABLY_EXECUTION_EXTRA", "[]")

    try:
        extension["extra"] = json.loads(extra)
    except Exception:
        logger.debug("Failed to parse RELIABLY_EXECUTION_EXTRA")
        extension["extra"] = []

    if "CI" in os.environ:
        repo = os.getenv("GITHUB_REPOSITORY")
        gh = os.getenv("GITHUB_SERVER_URL")
        run_id = os.getenv("GITHUB_RUN_ID")

        if repo and gh:
            extension["extra"].append(
                {
                    "type": "url",
                    "provider": "github",
                    "topic": "repo",
                    "value": f"{gh}/{repo}",
                }
            )

        if repo and gh and run_id:
            extension["extra"].append(
                {
                    "type": "url",
                    "provider": "github",
                    "topic": "run",
                    "value": f"{gh}/{repo}/actions/runs/{run_id}",
                }
            )


def set_plan_status(
    org_id: str,
    status: str,
    message: Optional[str],
    configuration: Configuration,
    secrets: Secrets,
) -> None:
    plan_id = os.getenv("RELIABLY_PLAN_ID")
    if not plan_id:
        return None

    logger.debug(f"Sending plan '{plan_id}' status: {status}")

    with get_session(configuration, secrets) as session:
        r = session.put(
            f"/{org_id}/plans/{plan_id}/status",
            json={"status": status, "error": message},
        )
        if r.status_code > 399:
            logger.debug(
                f"Failed to set plan status: {r.status_code}: {r.json()}"
            )


def set_execution_state(
    org_id: str,
    exp_id: str,
    exec_id: Optional[str],
    state: Dict[str, Any],
    configuration: Configuration,
    secrets: Secrets,
) -> None:
    if not exec_id:
        return None

    state["plan_id"] = os.getenv("RELIABLY_PLAN_ID")

    with get_session(configuration, secrets) as session:
        r = session.put(
            f"/{org_id}/experiments/{exp_id}/executions/{exec_id}/state",
            json=state,
        )
        if r.status_code > 399:
            logger.debug(
                f"Failed to set execution state: {r.status_code}: {r.json()}"
            )


def to_datetime(ts: str) -> datetime:
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%f").replace(
        tzinfo=timezone.utc
    )
