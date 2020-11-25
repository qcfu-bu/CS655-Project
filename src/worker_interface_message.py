# code related to typing and utilises for
# messages between the interface and worker
import json
from typing import NamedTuple, Union, Any


# the key for message type in the json
MSG_TYPE_NAME = "msg_type"


# to ping the worker when there is a new task
class NewTaskToWorkerMsg(NamedTuple):
    pass


# the respond from worker stating how many task it currently have
class WorkerTaskNumMsg(NamedTuple):
    task_num: int
    accepting_task: bool


# to send a task to the worker
class TaskAssignmentMsg(NamedTuple):
    img_file_name: str
    task_id: int


# the message when a worker finished with a task
class TaskFinishedMsg(NamedTuple):
    task_id: int


Message = Union[NewTaskToWorkerMsg, WorkerTaskNumMsg,
                TaskAssignmentMsg, TaskFinishedMsg]


# === My deepest apology to the younger purer me.
# === here comes the hacks:

def gen_message(msg: Message) -> str:
    """ Generate a string message from the given message

    :param msg: the input message
    :return: a json encoding of the input message
    """
    msg_dict = msg._asdict()
    msg_dict.update({MSG_TYPE_NAME: type(msg).__name__})

    return json.dumps(msg_dict)


def __parse_message_as(msg_type: type, msg_str: str) -> Any:
    """Parse a message as the given type.

    This is a private function, since the type information is not clear
    :param msg_type: the type to parse message as
    :param msg_str: the string to parse
    :return: a message object with the parsed message.
    """
    # parse the message
    msg_dict = json.loads(msg_str)

    # the type specified in the message needs to match
    # the type we are parsing as
    assert msg_dict[MSG_TYPE_NAME] == msg_type.__name__, \
        f"Message type did not match the parsing type," \
        f"parsing the message as type {msg_type.__name__}," \
        f"but get a message of type {msg_dict[MSG_TYPE_NAME]}"

    # remove the message type information, and create the object
    del msg_dict[MSG_TYPE_NAME]
    return msg_type(**msg_dict)


def parse_new_task_msg(msg_str: str) -> NewTaskToWorkerMsg:
    """parse a new task message

    This is just a wrapper for `__parse_message_as`
    to provide the type information
    """
    return __parse_message_as(NewTaskToWorkerMsg, msg_str)


def parse_worker_task_num_msg(msg_str: str) -> WorkerTaskNumMsg:
    """parse a worker task num message

    This is just a wrapper for `__parse_message_as`
    to provide the type information
    """
    return __parse_message_as(WorkerTaskNumMsg, msg_str)


def parse_task_assignment_msg(msg_str: str) -> TaskAssignmentMsg:
    """parse a task assignment message

    This is just a wrapper for `__parse_message_as`
    to provide the type information
    """
    return __parse_message_as(TaskAssignmentMsg, msg_str)


def parse_task_finished_msg(msg_str: str) -> TaskFinishedMsg:
    """parse a task finished message

    This is just a wrapper for `__parse_message_as`
    to provide the type information
    """
    return __parse_message_as(TaskFinishedMsg, msg_str)

