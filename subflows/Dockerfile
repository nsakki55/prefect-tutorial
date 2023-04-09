FROM prefecthq/prefect:2.8.7-python3.8
RUN pip install prefect-aws
RUN pip install s3fs
RUN pip install pandas

COPY ml_workflow_flow.py /opt/prefect/flows/ml_workflow_flow.py
