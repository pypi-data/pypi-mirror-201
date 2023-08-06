from airflow.operators.bash import BashOperator as AirflowBashOperator
from airflow.utils.context import Context
from airflow.exceptions import AirflowException, AirflowSkipException

from pathlib import Path
import json
import os


class BashOperator(AirflowBashOperator):

    def execute(self, context: Context):

        if self.cwd is not None:
            if not os.path.exists(self.cwd):
                raise AirflowException(f"Can not find the cwd: {self.cwd}")
            if not os.path.isdir(self.cwd):
                raise AirflowException(f"The cwd {self.cwd} must be a directory")
        env = self.get_env(context)

        ##### FLOWUI #####
        upstream_task_ids = [t.task_id for t in self.get_direct_relatives(upstream=True)]
        env.update({
            "AIRFLOW_CONTEXT_UPSTREAM_TASK_IDS": str(upstream_task_ids),
            "AIRFLOW_CONTEXT_DAG_RUN_ID": str(context["dag_run"].run_id)
        })

        upstream_xcoms = dict()
        for tid in upstream_task_ids:
            upstream_xcoms[tid] = context['ti'].xcom_pull(task_ids=tid) 
        
        # Save upstream tasks XCOM data in temp file
        xcom_in_file = Path("/opt/mnt/fs/tmp/xcom_input.json")
        with open(xcom_in_file, "w") as f:
            json.dump(upstream_xcoms, f, indent=4)
        ##################

        result = self.subprocess_hook.run_command(
            command=['bash', '-c', self.bash_command],
            env=env,
            output_encoding=self.output_encoding,
            cwd=self.cwd,
        )
        if self.skip_exit_code is not None and result.exit_code == self.skip_exit_code:
            raise AirflowSkipException(f"Bash command returned exit code {self.skip_exit_code}. Skipping.")
        elif result.exit_code != 0:
            raise AirflowException(
                f'Bash command failed. The command returned a non-zero exit code {result.exit_code}.'
            )

        ##### FLOWUI #####
        # Read from temporary file containing XCOM output
        xcom_out_file = Path("/opt/mnt/fs/tmp/xcom_output.json")
        with open(xcom_out_file) as f:
            xcom_out_dict = json.load(f)

        # Remove temporary files
        xcom_in_file.unlink()
        xcom_out_file.unlink()
        ##################
        return xcom_out_dict