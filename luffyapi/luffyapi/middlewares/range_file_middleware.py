import re
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve

class RangeFileMiddleware(MiddlewareMixin):
    """
    处理HTTP范围请求的中间件，支持文件部分内容传输（断点续传）。
    需配合支持流式响应的视图使用，为响应添加字节范围请求支持。

    主要功能：
    - 解析HTTP Range头，验证其格式并计算字节范围。
    - 根据范围请求生成部分响应内容，支持206 Partial Content状态码。
    - 对无效或超出范围的请求返回400 Bad Request或416 Range Not Satisfiable。
    """

    def process_response(self, request, response):
        """
        中间件的核心方法，处理响应对象以支持HTTP范围请求。

        参数:
            request: HttpRequest对象，包含客户端请求信息。
            response: HttpResponse对象，原始响应数据。

        返回:
            HttpResponse对象：
            - 如果未指定Range头或不满足条件，返回原始响应。
            - 如果范围请求有效，返回206 Partial Content响应。
            - 如果范围请求无效，返回400 Bad Request或416 Range Not Satisfiable。

        工作流程：
        1. 检查响应是否符合处理条件（仅处理200状态码且包含Content-Length）。
        2. 解析HTTP Range头，验证其格式并计算字节范围。
        3. 根据范围生成部分响应内容，并设置相关HTTP头。
        """
        resolver_match = resolve(request.path_info)
        view_func = resolver_match.func
        # 判断是否是类视图
        if hasattr(view_func, 'view_class'):
            view_class_name = view_func.view_class.__name__
        else:
            view_class_name = view_func.__name__
        # print("View class name:", view_class_name)

        # 仅当访问名为 CourseRetrieveAPIView 的视图时启用
        if view_class_name != 'serve':
            return response
        # 仅处理200状态码的响应且存在Content-Length
        if response.status_code != 200 or 'Content-Length' not in response:
            return response

        range_header = request.META.get('HTTP_RANGE')
        if not range_header:
            return response

        # 添加范围请求支持头，表明服务器支持字节范围请求
        response['Accept-Ranges'] = 'bytes'

        # 解析范围请求，获取起始和结束字节位置
        try:
            file_size = int(response['Content-Length'])
            start, end = self._parse_range_header(range_header, file_size)
        except ValueError:
            # 如果范围格式无效，返回400 Bad Request
            return HttpResponseBadRequest()

        # 检查起始位置是否超出文件大小
        if start >= file_size:
            return HttpResponse(status=416)

        # 调整结束位置，确保不超过文件大小
        if end is None or end >= file_size:
            end = file_size - 1

        # 检查起始位置是否大于结束位置
        if start > end:
            return HttpResponseBadRequest()

        # 构建范围响应，生成部分内容并设置相关HTTP头
        content_length = end - start + 1
        content = self._range_generator(response.streaming_content, start, end)
        response = HttpResponse(
            content,
            status=206,  # 表示部分内容响应
            content_type=response['Content-Type']
        )
        response['Content-Length'] = str(content_length)
        response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
        return response

    def _parse_range_header(self, range_header, file_size):
        """
        解析HTTP Range请求头，验证其格式并计算字节范围。

        参数:
            range_header: 字符串，原始Range请求头值。
            file_size: 整数，响应内容的总字节数。

        返回:
            包含两个整数的元组 (start, end)：
            - start: 起始字节位置（包含）。
            - end: 结束字节位置（包含），None表示到文件末尾。

        抛出:
            ValueError: 当范围格式无效或超出文件大小时。

        支持的Range头格式：
        - bytes=500-1000：从第500字节到第1000字节。
        - bytes=500-：从第500字节到文件末尾。
        - bytes=-500：最后500字节。
        """
        match = re.match(r'bytes=(\d+)?-(\d+)?', range_header)
        if not match:
            raise ValueError("Invalid range format")

        start_str, end_str = match.groups()
        if start_str is None and end_str is None:
            raise ValueError("Invalid range format")

        if start_str is None:
            # 处理 bytes=-500 格式（最后N字节）
            start = file_size - int(end_str)
            end = file_size - 1
        elif end_str is None:
            # 处理 bytes=500- 格式（从N字节到文件末尾）
            start = int(start_str)
            end = None
        else:
            # 处理 bytes=500-1000 格式（指定范围）
            start = int(start_str)
            end = int(end_str) if end_str else None

        # 验证范围边界是否合法
        if start < 0 or (end is not None and end < start):
            raise ValueError("Invalid range bounds")
        return (start, end)

    def _range_generator(self, streaming_content, start, end):
        """
        流式处理响应内容，生成指定字节范围的数据块。

        参数:
            streaming_content: 可迭代对象，原始响应内容数据流。
            start: 起始字节位置。
            end: 结束字节位置（None表示到文件末尾）。

        生成:
            bytes对象，按需截取的字节块。

        工作原理：
        - 遍历流式内容的每个数据块。
        - 计算当前块在整体内容中的位置。
        - 截取符合范围的部分并生成新的数据块。
        """
        current_pos = 0
        remaining = end - start + 1 if end is not None else None
        for chunk in streaming_content:
            chunk_size = len(chunk)
            # 计算当前块的起始和结束位置
            chunk_end = current_pos + chunk_size - 1

            # 如果当前块完全在范围之前，跳过
            if chunk_end < start:
                current_pos += chunk_size
                continue

            # 如果当前块完全在范围之后，停止处理
            if current_pos > end:
                break

            # 截取当前块中符合范围的部分
            start_in_chunk = max(start - current_pos, 0)
            end_in_chunk = chunk_size
            if end is not None:
                end_in_chunk = min(end - current_pos + 1, chunk_size)

            yield chunk[start_in_chunk:end_in_chunk]
            current_pos += chunk_size

            # 如果剩余字节数已处理完毕，停止生成
            if remaining is not None:
                remaining -= end_in_chunk - start_in_chunk
                if remaining <= 0:
                    break
