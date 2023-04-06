from prefect_aws.ecs import ECSTask, AwsCredentials

aws_credentials_block = AwsCredentials.load("default")

ecs = ECSTask(
    aws_credentials=aws_credentials_block,
    image="547760918250.dkr.ecr.ap-northeast-1.amazonaws.com/prod-flow:latest",
)
ecs.save("prod-ecs-task-block")