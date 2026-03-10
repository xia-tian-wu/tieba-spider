import asyncio
from PySide6.QtCore import Signal, QObject, QMetaObject, Qt
from logger import logger
from spider.tieba_spider import TiebaSpider

class AsyncWorker(QObject):
    """处理异步任务：同时支持新帖爬取和旧帖更新（并发处理）"""
    finished = Signal(list)  # 返回 [{url, status, data/error}, ...]
    error = Signal(str)      # 全局错误信息
    progress = Signal(str)   # 进度提示
    task_completed = Signal(str, str)  # url, task_type

    def __init__(self, new_urls=None, update_urls=None):
        super().__init__()
        self.spider = TiebaSpider()
        self.new_urls = new_urls or []
        self.update_urls = update_urls or []

    def run_async_task(self):
        """运行异步任务"""
        try:
            results = asyncio.run(self._run_crawl())
            # 清理爬虫对象
            self._cleanup_spider()
            # 发送完成信号
            self.finished.emit(results)
        except Exception as e:
            logger.error(f"异步任务执行失败：{e}")
            self._cleanup_spider()
            self.error.emit(str(e))

    def _cleanup_spider(self):
        """清理 spider 对象"""
        if hasattr(self, 'spider') and self.spider:
            try:
                # 只清理 httpx 客户端，不清理锁（避免跨线程问题）
                if self.spider.client and not self.spider.client.is_closed:
                    # 注意：这里不能 await，因为不在异步上下文中
                    # 所以只是将客户端引用置为 None，让 Python GC 处理
                    self.spider.client = None
            except Exception as e:
                logger.error(f"清理爬虫客户端失败：{e}")
            finally:
                self.spider = None

    async def _run_crawl(self):
        tasks = []
        for url in self.new_urls:
            tasks.append(self._crawl_new(url))
        for url in self.update_urls:
            tasks.append(self._update_existing(url))

        if not tasks:
            return []

        # 并发执行所有任务，捕获单个任务异常
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 格式化结果
        formatted_results = []
        for i, res in enumerate(results):
            if isinstance(res, Exception):
                formatted_results.append({
                    'url': self.new_urls[i] if i < len(self.new_urls) else self.update_urls[i - len(self.new_urls)],
                    'status': 'error',
                    'error': str(res)
                })
            else:
                formatted_results.append(res)
        return formatted_results

    async def _crawl_new(self, url):
        """处理新链接爬取"""
        self.progress.emit(f"爬取新帖：{url}")
        try:
            see_lz = 'see_lz=1' in url
            result = await self.spider.crawl_full_post(url, see_lz=see_lz)
            self.task_completed.emit(url, 'crawl')
            return {
                'url': url,
                'status': 'success' if result else 'failed',
                'data': result
            }
        except Exception as e:
            return {'url': url, 'status': 'error', 'error': str(e)}

    async def _update_existing(self, url):
        """处理旧链接更新"""
        self.progress.emit(f"更新旧帖：{url}")
        try:
            result = await self.spider.update_existed_post(url)
            self.task_completed.emit(url, 'update')
            return {
                'url': url,
                'status': 'updated' if result else 'skipped',
                'data': result
            }
        except Exception as e:
            return {'url': url, 'status': 'error', 'error': str(e)}
