# **Proxy Server with WAF Configuration**  
## **概要**
マイクロサービスごとに1つのプロキシサーバーを配置し、リクエストの適切なルーティングとセキュリティ対策を行います。  
各プロキシサーバーにはWAF (Web Application Firewall)を適用しており、悪意のあるリクエストを自動で検知・拒否します。

## **主な機能**
- リバースプロキシ: クライアントからのリクエストをマイクロサービスに転送
- WAF (Web Application Firewall) の適用:
  - SQLインジェクション、XSSなどの攻撃を防止
  - 不審なIPアドレスや異常なリクエストパターンをブロック

## **設定の仕組み**
- サーバー設定を **テンプレートファイル** を基に管理します。  
設定を変更する際は **必ずテンプレートファイルを編集** してください。  
- 設定ファイルは、対応するテンプレートファイル (`.template`) から自動生成されます。  
  **例:** `nginx.conf.template` → `nginx.conf`
- `.template` ファイル内の **環境変数** は展開され、値が設定されます。  
  - 環境変数が未設定の場合、デフォルト値が適用されます。

**注意:**  
`config` ファイルを直接編集しても、テンプレートファイルから上書きされるため、変更は反映されません。

## **以下のようにすることでWAFの設定をOFFにできます**
modsecurity.conf.template の line19 をOnからOffに
```
# -- Request body handling ---------------------------------------------------

# Allow ModSecurity to access request bodies. If you don't, ModSecurity
# won't be able to see any POST parameters, which opens a large security
# hole for attackers to exploit.
#
SecRequestBodyAccess Off
```