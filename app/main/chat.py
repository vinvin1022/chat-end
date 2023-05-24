import json
from random import choice, randint
import time
import uuid
from flask import request, Response
from extensions import db
from app.models.conversations import Conversations
from app.models.chats import Chats

from . import bp
from faker import Faker

fake = Faker()

conversation_history = []
conversation_history_relative = [
    {"cid": 1, "role": "user", "content": "content1", "name": "sheng", "children": 2},
    {
        "cid": 2,
        "role": "assistant",
        "content": "content1111",
        "name": "sheng",
        "parent": 1,
        "children": 3,
    },
    {
        "cid": 3,
        "role": "user",
        "content": "content1",
        "name": "sheng",
        "parent": 2,
        "children": 4,
    },
    {
        "cid": 4,
        "role": "assistant",
        "content": "content1",
        "name": "sheng",
        "parent": 3,
    },
]


roles = ["user", "assistant"]


@bp.route("/topic", methods=["GET"])
def topic():
    con = {
        "title": fake.name(),
        "parent": randint(1, 1000),
        "children": randint(1, 1000),
    }
    chat = Chats(**con)
    # print(chat.to_json())
    # 将用户对象添加到会话中
    db.session.add(chat)

    # 提交会话，将用户对象插入到数据库中
    db.session.commit()

    return {"code": 0, "data": con}


@bp.route("/chat1", methods=["GET"])
def chat1():
    print(request)
    print(Conversations)
    con = {
        "role": choice(roles),
        "content": fake.address(),
        "name": fake.name(),
        "parent": randint(1, 1000),
        "children": randint(1, 1000),
        "cid": randint(1, 1000),
    }
    conversation = Conversations(**con)
    # 将用户对象添加到会话中
    db.session.add(conversation)

    # 提交会话，将用户对象插入到数据库中
    db.session.commit()

    return {"code": 0, "data": con}


@bp.route("/chat", methods=["GET"])
def chat():
    content = request.args.get("content")
    # chatid = request.args.get("chatid")
    # title = request.args.get("title")
    full_reply_content = ""
    unique_id = str(uuid.uuid4())  # 生成一个随机的 UUID
    # 将用户输入添加到对话历史中
    conversation_history.append({"role": "user", "content": content, "name": "sheng"})
    single = {
        "role": "user",
        "content": content,
        "name": "sheng",
        "children": str(uuid.uuid4()),
    }

    if len(conversation_history_relative) >= 1:
        index = len(conversation_history_relative) - 1
        single["parent"] = conversation_history_relative[index].get("id")
        single["cid"] = conversation_history_relative[index].get("children")
    else:
        single["cid"] = str(uuid.uuid4())

    conversation_history_relative.append(single)
    print("conversation_history_relative: ", conversation_history_relative)

    def generate_events():
        # record the time before the request is sent
        start_time = time.time()

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history,
            temperature=0.6,
            stream=True,
            # prompt="\n".join(conversation_history),  # 将对话历史作为输入
        )
        collected_chunks = []
        collected_messages = []
        for chunk in response:
            chunk_time = (
                time.time() - start_time
            )  # calculate the time delay of the chunk
            if chunk["choices"][0]["finish_reason"] is not None:
                collected_messages.append("[DONE]")

                conversation_history.append(
                    {"role": "assistant", "content": full_reply_content}
                )

                single = {
                    # "id": str(uuid.uuid4()),
                    "role": "assistant",
                    "content": full_reply_content,
                    "children": str(uuid.uuid4()),
                }

                if len(conversation_history_relative) >= 1:
                    index = len(conversation_history_relative) - 1
                    print("index: ", index)
                    single["parent"] = conversation_history_relative[index].get("id")
                    # single["parent"] = str(uuid.uuid4())
                    single["cid"] = conversation_history_relative[index].get("children")
                else:
                    single["cid"] = str(uuid.uuid4())
                conversation_history_relative.append(single)
                print("conversation_history_relative: ", conversation_history_relative)

            else:
                # collected_chunks.append(chunk)  # save the event response
                chunk_message = chunk["choices"][0]["delta"].get(
                    "content", ""
                )  # extract the message
                collected_messages.append(chunk_message)  # save the message

            print(
                f"Message received {chunk_time:.2f} seconds after request: {chunk_message}"
            )  # print the delay and text

            full_reply_content = "".join([m for m in collected_messages])
            # yield f"data: {full_reply_content}\n\n"
            yield "data:{}\n\n".format(json.dumps(collected_messages))

        # print the time delay and text received
        print(f"Full response received {chunk_time:.2f} seconds after request")
        full_reply_content = "".join([m for m in collected_messages])
        print(f"Full conversation received: {full_reply_content}")

    response = Response(
        generate_events(), content_type="text/event-stream, charset=utf-8"
    )
    response.headers["Transfer-Encoding"] = "chunked"
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Connection"] = "keep-alive"
    return response

    return {"name": "Hello, world!"}
