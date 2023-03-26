from prefect.blocks.core import Block

json_block = Block.load("json/life-the-universe-everything")
print(json_block.value["the_answer"])
