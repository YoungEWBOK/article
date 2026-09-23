# AI 更新

网站地址：`https://yuxiyang.netlify.app/ai-updates/`。站点由 Netlify 从本仓库构建。

GitHub Actions 每天北京时间 09:17 运行 `scripts/update_ai_feed.py`，收集六个项目的官方 GitHub Releases 和两组 Google News 检索线索。公开数据写入 `static/ai-updates/data/updates.json`；小红书和微信公众号文案只生成在后台，并作为本次 Actions 运行的 artifact 保存 30 天。网站不展示草稿。

新闻检索结果是待核查线索，不保证覆盖全网。页面供读者搜索、筛选和关注来源。自动发帖与付费订阅均未启用；接入前需要平台账号的官方发布权限与相应账户配置。

可在仓库 Actions 中手动运行 `Refresh AI updates for Netlify` 检查数据采集。工作流更新 JSON 后推送仓库，由现有 Netlify 连接部署网站。
