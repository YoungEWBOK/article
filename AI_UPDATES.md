# AI 更新雷达

页面：`static/ai-updates/index.html`，发布后位于 `/article/ai-updates/`。

现有 GitHub Pages 工作流每天北京时间 09:17 运行 `scripts/update_ai_feed.py`，收集六个项目的官方 GitHub Releases 和两组 Google News 搜索线索。数据写入 `static/ai-updates/data/updates.json`，小红书及微信公众号文案草稿写入 `drafts/ai-updates/`。新闻搜索结果只是线索，不能视为官方公告，也不保证覆盖全网。

页面提供搜索、关注、近七天筛选和复制发布草稿。平台自动发帖尚未启用：小红书开放接口需要相应发布能力，公众号需要账号及发布接口权限。草稿须由账号持有人核对后发布。收费订阅与邮件发送也尚未接入。

可在仓库 Actions 中手动运行 `Deploy article site and refresh AI updates` 验证采集与发布。
