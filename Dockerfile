FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-runtime

RUN mkdir /main
WORKDIR /main

COPY gpt-j-6B-vietnamese-news ./gpt-j-6B-vietnamese-news

COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt

COPY scripts ./scripts
RUN chmod +x ./scripts/*.sh

COPY src ./src

EXPOSE 5000
CMD ["./scripts/run_service.sh"]
