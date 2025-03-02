# proxy server with WAF configured
## 説明
- サーバーの設定をする際は、templateファイルを変更する  
**WARN: configファイルを直接修正しない. configファイルを修正しても、templateファイルに上書きされる**
- templateファイルからconfigファイルが生成される. ex) `nginx.conf.template`から`nginx.conf`が生成される
- templateファイル内の環境変数は展開される.設定していない環境変数はデフォルトの値が適応される
