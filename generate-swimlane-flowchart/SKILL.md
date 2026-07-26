---
name: flow-designer-yongdao
description: Convert business process descriptions into swimlane flowcharts, structured flow.json data, and draw.io diagrams. Use when the user asks to analyze a business workflow, assign responsibilities to lanes, model decisions, documents, databases, APIs, or subprocesses, or generate/update a swimlane diagram from process text.
---

# 泳道流程图生成

## 何时使用
- 将业务描述整理为泳道流程图。
- 将角色、系统、审批、数据库、外部接口映射到不同泳道。
- 生成或更新 `scripts/flow.json`，并输出 `scripts/output/flow.drawio`。
- 支持将结果同时输出到业务项目目录。

## 工作流程
1. 先读取 `references/flow-rules.md` 和 `references/flow_demo.json`，确认数据结构和建模规则。
2. 从用户输入中提取业务目标、参与角色、动作、文档、数据对象和判断规则。
3. 按规则生成 `scripts/flow.json`。
4. 运行 `python main.py` 生成 `scripts/output/flow.drawio`。如需同时输出到业务项目目录，从以下方式中任选其一（优先级从高到低）：
   - **`--project-output-file <完整路径>`**：直接指定输出文件路径（含文件名）
   - **`--project-output-dir <项目目录>`**：指定目录，自动追加 `flow.drawio`
   - **环境变量 `FLOW_OUTPUT_FILE`**：等价于 `--project-output-file`
   - **环境变量 `FLOW_OUTPUT_DIR`**：等价于 `--project-output-dir`
   
   例如：
   ```bash
   # 方式1：指定完整路径
   python main.py --project-output-file D:/my-project/docs/流程图.drawio

   # 方式2：只指定目录
   python main.py --project-output-dir D:/my-project/docs

   # 方式3：配合环境变量（项目级 .env 或系统变量）
   set FLOW_OUTPUT_DIR=D:/my-project/docs
   python main.py
   ```
5. 如有需要，再根据人工反馈微调布局或节点文案。

## 约束
- 一条泳道只表示一个责任主体。
- 不要混用部门、岗位和系统名称。
- 所有任务、判断和结果都必须放在对应泳道内。
- Start 放在左上方，流程按时间顺序推进。
- 节点文案保持简短明确。

## 参考
- `references/flow-rules.md`：详细建模与排版规则。
- `references/flow_demo.json`：示例输入数据。



