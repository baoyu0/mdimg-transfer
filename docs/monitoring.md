# 监控系统文档

## 概述

mdimg-transfer 的监控系统提供了全面的性能指标和状态监控功能，帮助用户了解应用的运行状况、性能瓶颈和资源使用情况。系统集成了 Prometheus 指标收集，并提供了实时的 WebSocket 进度通知。

## 监控组件

### 1. 指标收集器

#### 系统指标 (SystemMetrics)
- 内存使用
- CPU 使用率
- 磁盘使用情况

#### 缓存指标 (CacheMetrics)
- 缓存大小
- 命中/未命中统计
- 操作状态

#### 处理指标 (ProcessingMetrics)
- 处理时间
- 成功/失败率
- 图片大小统计

#### 队列指标 (QueueMetrics)
- 队列大小
- 等待时间
- 处理延迟

### 2. WebSocket 实时通知

- 处理进度更新
- 状态变更通知
- 错误报告

## 指标详情

### 系统指标

| 指标名称 | 类型 | 标签 | 说明 |
|----------|------|------|------|
| memory_usage_bytes | Gauge | - | 内存使用量 |
| cpu_usage_percent | Gauge | - | CPU 使用率 |
| disk_usage_bytes | Gauge | path | 磁盘使用量 |

### 缓存指标

| 指标名称 | 类型 | 标签 | 说明 |
|----------|------|------|------|
| cache_operations_total | Counter | operation, status | 缓存操作计数 |
| cache_size | Gauge | - | 当前缓存大小 |

### 处理指标

| 指标名称 | 类型 | 标签 | 说明 |
|----------|------|------|------|
| processed_images_total | Counter | status | 处理图片总数 |
| processing_duration_seconds | Histogram | - | 处理时间分布 |
| processed_bytes_total | Counter | type | 处理字节数 |

### 队列指标

| 指标名称 | 类型 | 标签 | 说明 |
|----------|------|------|------|
| queue_size | Gauge | - | 当前队列大小 |
| queue_latency_seconds | Histogram | - | 队列等待时间 |

## 监控端点

### Prometheus 端点

```
GET /metrics
```

返回 Prometheus 格式的指标数据。

### 统计端点

```
GET /stats
```

返回 JSON 格式的处理统计信息：
```json
{
    "total_processed": 1000,
    "success_rate": 98.5,
    "average_processing_time": 0.5,
    "total_bytes_processed": 1024000,
    "cache_hit_rate": 85.2
}
```

### 历史记录端点

```
GET /history
```

返回处理历史记录：
```json
{
    "records": [
        {
            "id": "123",
            "timestamp": "2024-01-20T10:00:00Z",
            "original_url": "http://example.com/image.jpg",
            "processed_url": "https://cdn.example.com/image.jpg",
            "processing_time": 0.5,
            "status": "success"
        }
    ]
}
```

## WebSocket 通知

### 连接

```
WS /ws/<client_id>
```

### 消息格式

```json
{
    "type": "progress",
    "data": {
        "task_id": "123",
        "progress": 75,
        "status": "processing",
        "message": "处理第 3/4 个图片"
    }
}
```

## 监控面板

### Prometheus + Grafana

1. 配置 Prometheus 数据源：
```yaml
scrape_configs:
  - job_name: 'mdimg-transfer'
    static_configs:
      - targets: ['localhost:9090']
```

2. 导入 Grafana 仪表板：
- 系统监控面板
- 处理性能面板
- 缓存状态面板

## 告警配置

### 系统告警

```yaml
groups:
- name: mdimg-transfer
  rules:
  - alert: HighMemoryUsage
    expr: memory_usage_bytes > 1e9
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: 内存使用过高

  - alert: HighCpuUsage
    expr: cpu_usage_percent > 80
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: CPU 使用率过高
```

### 业务告警

```yaml
  - alert: LowSuccessRate
    expr: success_rate < 95
    for: 15m
    labels:
      severity: critical
    annotations:
      summary: 处理成功率过低

  - alert: HighProcessingTime
    expr: avg_processing_time > 2
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: 处理时间过长
```

## 最佳实践

### 1. 指标收集

- 合理设置采样频率
- 避免收集过多指标
- 使用适当的指标类型
- 添加有意义的标签

### 2. 告警配置

- 设置合适的阈值
- 避免告警风暴
- 分级告警策略
- 提供清晰的告警信息

### 3. 监控维护

- 定期检查指标有效性
- 及时更新告警规则
- 清理历史数据
- 优化存储空间

## 故障排查

### 1. 性能问题

检查指标：
- 处理时间趋势
- 资源使用情况
- 队列积压情况

### 2. 内存泄漏

监控指标：
- 内存使用趋势
- 缓存大小变化
- GC 频率

### 3. 并发问题

关注指标：
- 队列等待时间
- 处理并发数
- 错误率变化

## 未来改进

1. **监控增强**
   - 添加更多业务指标
   - 优化指标收集性能
   - 提供更详细的分析

2. **可视化改进**
   - 自定义仪表板
   - 交互式图表
   - 实时状态展示

3. **告警优化**
   - 智能告警阈值
   - 告警聚合
   - 自动故障分析
