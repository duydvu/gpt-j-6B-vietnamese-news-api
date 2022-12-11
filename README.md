# API service for GPT-J 6B on Vietnamese News

This Python code run an API service to make inference with [GPT-J 6B on Vietnamese News](https://huggingface.co/VietAI/gpt-j-6B-vietnamese-news).

Although the model is gigantic, I have managed to run it on a 16GB node with 2 x NVIDIA T4 on GKE. Using spot node decreases the cost down to about $180/month or $0.25/hour, which is a relatively cheap price if we want to run it occasionally.

## Build Docker

First, you need to download the model to local.
1. Install git-lfs
2. Run `git clone https://huggingface.co/VietAI/gpt-j-6B-vietnamese-news`

Next, move the model folder into this repository folder:
```
mv ./gpt-j-6B-vietnamese-news ./gpt-j-6B-vietnamese-news-api
```

And build Docker image:
```
docker build -t gpt-j .
```

## Run API service

Run with Docker:
```
docker run -it --rm -p 5000:5000 gpt-j
```

Deploy with Helm:
```
helm install --set namespace=default --set image=gpt-j --set version=latest gpt-j ./k8s/chart
```

## Test API

To make inference, call HTTP POST method to `/predict` with JSON body, for example:
```
{
    "text": "Tiềm năng của trí tuệ nhân tạo",
    "n_samples": 1
}
```

Result:
```
{
    "generated_texts": [
        "Tiềm năng của trí tuệ nhân tạo là rất lớn, nhiều ứng dụng có thể ra đời trong tương lai không xa, và điều đó đòi hỏi sự nỗ lực của cả cộng đồng.\nMột điểm khác cần lưu ý là trí tuệ nhân tạo là một lĩnh vực phát triển hoàn toàn mới và không thể chỉ dựa vào mỗi việc nghiên cứu của các trường, viện mà phải kết hợp với các doanh nghiệp, và phải có sự kết nối mạnh mẽ với các doanh nghiệp.\nVề việc chuẩn bị nhân lực cho cuộc cách mạng công nghiệp lần thứ 4, Phó Thủ tướng lưu ý các trường cần có sự đổi mới về cơ chế, phương pháp, mô hình dạy và học nhằm tạo môi trường tốt nhất cho trí tuệ nhân tạo.\n\"Nếu cứ làm theo cách cũ thì các trường sẽ như\"rúc thóc\"vào bao, nhưng nếu áp dụng phương pháp mới mà các trường chưa có, mới ở giai đoạn đầu mà có quy mô lớn hơn nhiều lần thì sẽ rất khó khăn\", Phó Thủ tướng chia sẻ.\nPhó Thủ tướng Vũ Đức Đam đề nghị Bộ KH&CN tiếp tục có sự phối hợp với các bộ, ngành, trước hết là Bộ KH&CN xây dựng chiến lược, quy hoạch phát triển, thực hiện đề án tăng cường"
    ]
}
```

Beside `text` param, there are 3 more params:
1. `n_samples`: number of samples to return. Default: `10`.
2. `top_k`: filter k most likely next words. Default: `50`.
3. `top_p`: chooses from the smallest possible set of words whose cumulative probability exceeds the probability p. Default: `0.9`.

The method of generating texts is sampling the next words from a probability distribution from the output of the model. So everytime the API is called, it will generate different results.

See [https://huggingface.co/blog/how-to-generate](https://huggingface.co/blog/how-to-generate) to understand about `top_k` and `top_p`.
