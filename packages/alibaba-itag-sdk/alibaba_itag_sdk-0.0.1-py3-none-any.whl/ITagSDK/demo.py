import time
import uuid
from ITagSDK import ItagSdk, Config, AlphaDataSdk, alpha_data_models, itag_models

if __name__ == '__main__':
    tenant_id = ""
    tenant_token = """-----BEGIN RSA PRIVATE KEY-----
-----END RSA PRIVATE KEY-----
"""
    employee_id = ""

    itag = ItagSdk(
        config=Config(
            tenant_id, tenant_token, endpoint="itag2.alibaba-inc.com"
        ),
        buc_no=employee_id
    )

    alphad = AlphaDataSdk(
        config=Config(
            tenant_id, tenant_token, endpoint="alphad.alibaba-inc.com"
        ),
        buc_no=employee_id
    )

    """
    创建数据集
    """
    with open(r"filePath\test.csv", "rb") as file:
        create_dataset_response = alphad.create_dataset(
            tenant_id,
            alpha_data_models.CreateDatasetRequest(
                data_source="LOCAL_FILE",
                dataset_name="dataset_name",
                owner_name="owner_name",
                owner_employee_id=employee_id,
                file_name="file_name.csv",
                file=file,
                content_type="multipart/form-data",
                secure_level=1,
                remark="remark"
            )
        )

    # 等待数据集就绪
    dataset_id = create_dataset_response.body.result
    while True:
        dataset_response = alphad.get_dataset(tenant_id, str(dataset_id))
        status = dataset_response.body.result.status

        if not status:
            raise ValueError("dataset status error")

        if status == "FINISHED":
            break

        time.sleep(5)

    """
    创建模板
    """
    create_template_request = itag_models.CreateTemplateRequest(
        body=itag_models.TemplateDTO(
            view_configs=itag_models.TemplateDTOViewConfigs(
                view_plugins=[
                    itag_models.ViewPlugin(
                        hide=False,
                        bind_field='url',
                        type='IMG',
                        cors_proxy=False,
                        visit_info=itag_models.ViewPluginVisitInfo(),
                        display_ori_img=True
                    )
                ]
            ),
            question_configs=[
                itag_models.QuestionPlugin(
                    options=[
                        itag_models.QuestionOption(
                            label='人',
                            key='1'
                        ),
                        itag_models.QuestionOption(
                            label='动物',
                            key='2'
                        ),
                        itag_models.QuestionOption(
                            label='植物',
                            key='3'
                        )
                    ],
                    type='RADIO',
                    question_id='55',
                    must_fill=False,
                    mark_title='全局单选',
                    display=True
                )
            ],
            template_name='图片分类模板'
        )
    )
    template_response = itag.create_template(tenant_id, create_template_request)

    """
    创建任务
    """
    source_dataset_id = dataset_response.get("result")
    create_task_request = itag_models.CreateTaskRequest(
        body=itag_models.CreateTaskDetail(
            task_name='测试任务',
            template_id=template_response.body.template_id,
            task_workflow=[
                itag_models.CreateTaskDetailTaskWorkflow(
                    node_name='MARK'
                )
            ],
            admins=itag_models.CreateTaskDetailAdmins(),
            assign_config=itag_models.TaskAssginConfig(
                assign_count=1,
                assign_type='FIXED_SIZE'
            ),
            uuid=str(uuid.uuid4()),
            task_template_config=itag_models.TaskTemplateConfig(),
            dataset_proxy_relations=[
                itag_models.DatasetProxyConfig(
                    source_dataset_id=str(source_dataset_id),
                    dataset_type='LABEL',
                    source='ALPHAD'
                )
            ]
        )
    )
    create_task_response = itag.create_task(tenant_id, create_task_request)

    """
    任务人力信息变更
    """
    task_id = create_task_response.body.task_id
    task_workforce = itag.get_task_workforce(tenant_id, task_id)
    # workforce 一般为多个根据任务流程来判断[标注-质检-验收][标注-验收]等
    # 具体可以根据 workforce[0].node_type 字段判断任务类型
    work_node_id = task_workforce.body.workforce[0].work_node_id
    itag.add_work_node_workforce(
        tenant_id, task_id, str(work_node_id), itag_models.AddWorkNodeWorkforceRequest(
            [itag_user_id]
        )
    )

    """
    获取任务结果
    """
    anno_response = itag.export_annotations(tenant_id, task_id, itag_models.ExportAnnotationsRequest())
    job_id = anno_response.body.flow_job.job_id
    job_request = itag_models.GetJobRequest(
        job_type="DOWNLOWD_MARKRESULT_FLOW"
    )
    # 等待标注结果生成
    while True:
        job_response = itag.get_job(tenant_id, job_id, request=job_request)
        status = job_response.body.job.status

        if status != ["init", "running", "succ"]:
            raise ValueError(job_response.body.message)

        if status == "succ":
            # 打印标注结果链接地址
            print(job_response.body.job.job_result.result_link)
            break

        time.sleep(3)

