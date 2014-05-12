###GET /search

参数

    word -- 查询词语 必选
    subject -- 所属分类 可选

return

    word -- 根据查询词语模糊搜所后的word
    raw_data -- word对应的原始数据
    trans -- word对应的所有翻译

    {
        "raw_data": [
            {
                "url": "http://www.paper.edu.cn/html/releasepaper/2014/04/78/",
                "subject_id": 21,
                "title_en": "Preparation and Study on Structural Radar-Absorbing Material Made by 3D Printing Technology",
                "id": 525,
                "subject": "材料科学"
            }
        ],
        "trans": [
            {
                "raw_data": [
                    {
                        "url": "http://www.paper.edu.cn/html/releasepaper/2014/04/78/",
                        "subject_id": 21,
                        "id": 525,
                        "title_cn": "3D打印技术制备结构吸波材料及其性能研究",
                        "subject": "材料科学"
                    }
                ],
                "id": 3,
                "word": "吸波材料"
            }
        ],
        "id": 3,
        "word": "absorbing material",
        "cn_word": [
            3
        ]
    },
