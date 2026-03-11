# extract-papers
从网页上提取论文信息到表格

# 环境
```shell
conda create -n extract-papers python=3.11 -y
conda activate extract-papers
# 安装from bs4 import BeautifulSoup
pip install bs4 lxml

```

# 数据来源
`https://papers.cool/venue/ICLR.2026?show=10000`

# 后续操作
附件给LLM，提示词：
```
增加列tldr_zh：根据summary，用1句中文凝练论文；
增加列category：根据summary和keywords给论文分类，例如RAG、Agent；
保持其他列不变，输出扩展后的csv文件。
```
