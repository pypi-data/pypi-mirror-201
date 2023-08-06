import json

import ai.h2o.featurestore.api.v1.CoreService_pb2 as pb

from ..utils import Utils


class ScheduledTask:
    def __init__(self, stub, scheduled_task):
        st = pb.ScheduledTask()
        st.CopyFrom(scheduled_task)
        self._scheduled_task = st
        self._stub = stub

    @property
    def id(self):
        return self._scheduled_task.id

    @property
    def name(self):
        return self._scheduled_task.name

    @property
    def description(self):
        return self._scheduled_task.description

    @description.setter
    def description(self, value: str):
        update_request = pb.ScheduledTaskUpdateRequest(
            scheduled_task_id=self._scheduled_task.id,
            description=value,
            updated_fields=["description"],
        )
        self._stub.UpdateScheduledTask(update_request)
        self._refresh()

    @property
    def schedule(self):
        return self._scheduled_task.schedule

    @schedule.setter
    def schedule(self, value: str):
        update_request = pb.ScheduledTaskUpdateRequest(
            scheduled_task_id=self._scheduled_task.id,
            schedule=value,
            updated_fields=["schedule"],
        )
        self._stub.UpdateScheduledTask(update_request)
        self._refresh()

    def delete(self):
        request = pb.ScheduledTaskId(scheduled_task_id=self._scheduled_task.id)
        self._stub.DeleteScheduledTask(request)

    def _refresh(self):
        request = pb.ScheduledTaskId(scheduled_task_id=self._scheduled_task.id)
        response = self._stub.GetScheduledTask(request)
        self._scheduled_task = response.task

    def __repr__(self):
        last_exec = (
            ""
            if self._scheduled_task.last_exec.seconds == 0
            else Utils.convert_timestamp_to_str_with_zone(self._scheduled_task.last_exec)
        )
        last_update_time = (
            ""
            if self._scheduled_task.last_update_date_time.seconds == 0
            else Utils.convert_timestamp_to_str_with_zone(self._scheduled_task.last_update_date_time)
        )
        task_type = pb.TaskType.DESCRIPTOR.values_by_number.get(self._scheduled_task.task_type).name
        task = {
            "id": self._scheduled_task.id,
            "name": self._scheduled_task.name,
            "description": self._scheduled_task.description,
            "feature_set_id": self._scheduled_task.feature_set_id,
            "project_id": self._scheduled_task.project_id,
            "source": json.loads(Utils.pretty_print_proto(self._scheduled_task.source)),
            "schedule": self._scheduled_task.schedule,
            "next_run_time": Utils.convert_timestamp_to_str_with_zone(self._scheduled_task.next_run_time),
            "last_exec": last_exec,
            "owner": json.loads(Utils.pretty_print_proto(self._scheduled_task.owner)),
            "created_date_time": Utils.convert_timestamp_to_str_with_zone(self._scheduled_task.created_date_time),
            "last_update_date_time": last_update_time,
            "task_type": task_type,
            "feature_set_version": self._scheduled_task.feature_set_version,
        }
        return json.dumps(task, indent=2)

    def __str__(self):
        return (
            f"Name                  : {self.name} \n"
            f"Description           : {self.description} \n"
            f"Feature set version   : {self._scheduled_task.feature_set_version} \n"
            f"Owner                   \n{self._custom_user_string()}"
            f"Source                  \n{self._custom_source_string()}"
            f"Schedule              : {self.schedule} \n"
            f"Last execution        : {self._scheduled_task.last_exec} \n"
            f"Next run time         : {self._scheduled_task.next_run_time}"
        )

    def _custom_user_string(self):
        return (
            f"          Name        : {self._scheduled_task.owner.name} \n"
            f"          Email       : {self._scheduled_task.owner.email} \n"
        )

    def _custom_source_string(self):
        source_dict = Utils.proto_to_dict(self._scheduled_task.source)
        source = list(source_dict.keys())[0]
        tmp_str = ""
        for key, value in source_dict.get(source).items():
            tmp_str = tmp_str + Utils.output_indent_spacing(f"{key}: {value} \n", "           ")

        return (
            f"{Utils.output_indent_spacing(source, '       ')}: [ \n"
            f"{tmp_str}"
            f"{Utils.output_indent_spacing(']', '       ')} \n"
        )
