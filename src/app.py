# -*- coding: utf-8 -*-
import gradio as gr
import time
import json
import random


# 加载对话历史数据
def load_dialog_history(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        dialog_history = [json.loads(line) for line in file]
    return dialog_history


# 加载诊断结果数据
def load_diagnosis_results(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        diagnosis_results = [json.loads(line) for line in file]
    return diagnosis_results


# 示例文件路径
dialog_history_file = './outputs/dialog_history_iiyi/dialog_history_gpt4.jsonl'
diagnosis_results_file = './outputs/collaboration_history_iiyi/doctors_2_agent_gpt3_gpt4_parallel_with_critique_discussion_history.jsonl'

# 加载数据
dialog_history = load_dialog_history(dialog_history_file)
diagnosis_results = load_diagnosis_results(diagnosis_results_file)

# 获取所有可用的patient_id
patient_ids = list(set(entry["patient_id"] for entry in dialog_history))


# 定义一个函数来逐步显示对话历史
def display_dialog(patient_id):
    dialog_text = []
    patient_dialog_history = [entry for entry in dialog_history if entry["patient_id"] == patient_id][0][
        "dialog_history"]
    for entry in patient_dialog_history:
        if entry['role'] == "Doctor":
            dialog_text.append(("Doctor", entry['content']))
        else:
            dialog_text.append(("Patient", entry['content']))
        yield dialog_text, "", ""  # 返回对话内容和空的诊断结果
        time.sleep(1)  # 模拟逐步输出的延迟


# 定义一个函数来逐步显示检查结果
def display_examiner_results(patient_id):
    result_text = ""
    patient_diagnosis_results = [entry for entry in diagnosis_results if entry["patient_id"] == patient_id][0]
    for result in patient_diagnosis_results['symptom_and_examination'].split('\n'):
        result_text += f"{result}\n\n"
        yield result_text
        time.sleep(1)  # 模拟逐步输出的延迟


# 定义一个函数来逐步显示最终讨论结果
def display_final_result(patient_id):
    patient_diagnosis_results = [entry for entry in diagnosis_results if entry["patient_id"] == patient_id][0]
    diagnosis = patient_diagnosis_results["diagnosis"]
    symptoms_and_examinations = patient_diagnosis_results["symptom_and_examination"]
    full_text = f"{diagnosis}\n\n{symptoms_and_examinations}"

    result_text = ""
    for i in range(0, len(full_text), 20):
        result_text += full_text[i:i + 20]
        yield result_text
        time.sleep(1)  # 每秒输出5个字


# 定义一个函数来更新对话
def update_dialog():
    patient_id = random.choice(patient_ids)
    dialog = []
    for dialog, _, _ in display_dialog(patient_id):
        yield dialog, "", ""  # 返回对话内容和空的诊断结果
    for examiner_result in display_examiner_results(patient_id):
        yield dialog, examiner_result, ""  # 逐步返回检查结果
    for final_result_text in display_final_result(patient_id):
        yield dialog, examiner_result, final_result_text  # 逐步返回诊断结果


# 定义一个函数来重置对话
def reset_dialog():
    return [], "", ""


# 创建Gradio界面
with gr.Blocks() as demo:
    gr.Markdown("# AI医院: Multi-Agent 医学智能体")
    with gr.Row():
        with gr.Column(scale=3):
            gr.Image("../assets/demo.png",height=300, width=1200, label="AI Hospital")
    gr.Markdown("""
                        与患者进行多轮对话，提出相关和探索性的问题，推荐适当的医学检查，并在收集足够的信息后做出诊断。设置检查员，他们专门负责与患者互动并提供相关的医学检查结果，确保医生能够获得患者必要的客观信息以做出准确诊断。此外，主治医生负责在整个会话后评估医生的表现。
                        模拟患者与多名医生之间的互动，包括体检结果的收集和最终诊断。
                        该系统使用先进的人工智能模型来模拟现实的医疗场景。""")

    with gr.Row():
        with gr.Column(scale=1):
            start_button = gr.Button("开始")
            reset_button = gr.Button("重置")
        with gr.Column(scale=4):
            chatbot = gr.Chatbot(label="Doctor chat with Patient ")
            examiner_output = gr.Textbox(label="Examiner(检查员)", lines=10)
            result_output = gr.Textbox(label="主任医师（Chief Physician）协作诊疗", lines=20, interactive=False)

    start_button.click(update_dialog, inputs=None, outputs=[chatbot, examiner_output, result_output])
    reset_button.click(reset_dialog, inputs=None, outputs=[chatbot, examiner_output, result_output])
    # 添加图片和文字说明


# 启动Gradio应用
demo.launch(enable_queue=True)






