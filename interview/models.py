from django.contrib.auth.models import User
from django.db import models
from django.utils.html import format_html


# 一面结果
INTERVIEW_RESULT_TYPE = [
    ('建议复试', '建议复试'),
    ('待定', '待定'),
    ('放弃', '放弃')
]

# 复试面试建议
HR_INTERVIEW_RESULT_TYPE = [
    ('建议录用', '建议录用'),
    ('待定', '待定'),
    ('放弃', '放弃')
]

# 候选人学历
DEGREE_TYPE = [
    ('本科', '本科'),
    ('硕士', '硕士'),
    ('博士', '博士')
]

# HR终面结论
HR_SCORE_TYPE = [
    ('S', 'S'),
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C')
]


class Candidate(models.Model):
    # 基础性息
    userid = models.IntegerField(unique=True, blank=True, null=True, verbose_name="应聘者ID")
    username = models.CharField(max_length=125, verbose_name="姓名")
    city = models.CharField(max_length=125, verbose_name="城市")
    phone = models.CharField(max_length=125, verbose_name="手机号码")
    email = models.EmailField(max_length=125, blank=True, verbose_name="邮箱")
    apply_position = models.CharField(max_length=125, blank=True, verbose_name="应聘职位")
    born_address = models.CharField(max_length=125, blank=True, verbose_name="生源地")
    gender = models.CharField(max_length=125, blank=True, verbose_name="性别")
    candidate_remark = models.CharField(max_length=125, blank=True, verbose_name="候选人备注")

    # 学校与学历信息
    bachelor_school = models.CharField(max_length=125, blank=True, verbose_name="本科院校")
    master_school = models.CharField(max_length=125, blank=True, verbose_name="研究生院校")
    doctor_school = models.CharField(max_length=125, blank=True, verbose_name="博士生院校")
    major = models.CharField(max_length=125, blank=True, verbose_name="专业")
    degree = models.CharField(max_length=125, choices=DEGREE_TYPE, blank=True, verbose_name="学历")

    # 综合能力评测成绩、笔试评测成绩
    test_score_of_general_ability = models.DecimalField(decimal_places=1, max_digits=3, null=True, blank=True,
                                                        verbose_name="综合能力评测成绩",
                                                        help_text="00.0-99.9")
    paper_score = models.DecimalField(decimal_places=1, max_digits=3, null=True, blank=True, verbose_name="笔试成绩",
                                      help_text="00.0-99.9")

    # 第一轮面试记录
    first_score = models.DecimalField(decimal_places=1, max_digits=2, null=True, blank=True, verbose_name="初试成绩",
                                      help_text="0.0-9.9 >=9.0极优秀  8.0-8.9优秀  7.0-7.9良好  6.0-6.9一般  <=5.9较差")
    first_learning_ability = models.DecimalField(decimal_places=1, max_digits=2, null=True, blank=True,
                                                 verbose_name="学习能力成绩",
                                                 help_text="0.0-9.9")
    first_professional_competency = models.DecimalField(decimal_places=1, max_digits=2, null=True, blank=True,
                                                        verbose_name="专业能力成绩",
                                                        help_text="0.0-9.9")
    first_advantage = models.TextField(max_length=1024, blank=True, verbose_name="优势")
    first_disadvantage = models.TextField(max_length=1024, blank=True, verbose_name="顾虑与不足")
    first_result = models.CharField(max_length=256, choices=INTERVIEW_RESULT_TYPE, blank=True,
                                    verbose_name="初步结果")
    first_recommend_position = models.CharField(max_length=256, blank=True, verbose_name="推荐部门")
    first_interviewer_user = models.ForeignKey(User, related_name="first_interviewer_user", null=True, blank=True,
                                               on_delete=models.CASCADE, verbose_name="一面面试官")
    first_remark = models.CharField(max_length=256, blank=True, verbose_name="初试备注")

    # 第二轮面试记录
    second_score = models.DecimalField(decimal_places=1, max_digits=2, null=True, blank=True,
                                       verbose_name="专业复试成绩",
                                       help_text="0.0-9.9 >=9.0极优秀  8.0-8.9优秀  7.0-7.9良好  6.0-6.9一般  <=5.9较差")
    second_learning_ability = models.DecimalField(decimal_places=1, max_digits=2, null=True, blank=True,
                                                  verbose_name="学习能力成绩",
                                                  help_text="0.0-9.9")
    second_professional_competency = models.DecimalField(decimal_places=1, max_digits=2, null=True, blank=True,
                                                         verbose_name="专业能力成绩",
                                                         help_text="0.0-9.9")
    second_pursue_of_excellence = models.DecimalField(decimal_places=1, max_digits=2, null=True, blank=True,
                                                      verbose_name="追求卓越成绩",
                                                      help_text="0.0-9.9")
    second_communication_ability = models.DecimalField(decimal_places=1, max_digits=2, null=True, blank=True,
                                                       verbose_name="沟通能力成绩",
                                                       help_text="0.0-9.9")
    second_pressure_score = models.DecimalField(decimal_places=1, max_digits=2, null=True, blank=True,
                                                verbose_name="抗压能力成绩",
                                                help_text="0.0-9.9")
    second_advantage = models.TextField(max_length=1024, blank=True, verbose_name="优势")
    second_disadvantage = models.TextField(max_length=1024, blank=True, verbose_name="顾虑与不足")
    second_result = models.CharField(max_length=256, choices=INTERVIEW_RESULT_TYPE, blank=True,
                                     verbose_name="专业复试结果")
    second_recommend_position = models.CharField(max_length=256, blank=True, verbose_name="推荐方向或推荐部门")
    second_interviewer_user = models.ForeignKey(User, related_name="second_interviewer_user", null=True, blank=True,
                                                on_delete=models.CASCADE, verbose_name="二面面试官")
    second_remark = models.CharField(max_length=256, blank=True, verbose_name="专业面试备注")

    # HR终面
    hr_score = models.CharField(max_length=10, choices=HR_SCORE_TYPE, blank=True,
                                verbose_name="HR复试综合等级",
                                help_text="S极优秀  A优秀  B良好  C一般")
    hr_responsibility = models.CharField(max_length=10, choices=HR_SCORE_TYPE, blank=True, verbose_name="HR责任心")
    hr_communication_ability = models.CharField(max_length=10, choices=HR_SCORE_TYPE, blank=True, verbose_name="HR坦诚沟通")
    hr_logic_ability = models.CharField(max_length=10, choices=HR_SCORE_TYPE, blank=True, verbose_name="HR逻辑思维")
    hr_potential = models.CharField(max_length=10, choices=HR_SCORE_TYPE, blank=True, verbose_name="HR发展潜力")
    hr_stability = models.CharField(max_length=10, choices=HR_SCORE_TYPE, blank=True, verbose_name="HR稳定性")
    hr_advantage = models.TextField(max_length=1024, blank=True, verbose_name="优势")
    hr_disadvantage = models.TextField(max_length=1024, blank=True, verbose_name="顾虑与不足")
    hr_result = models.CharField(max_length=256, choices=HR_INTERVIEW_RESULT_TYPE, blank=True,
                                 verbose_name="HR复试结果")
    hr_interviewer_user = models.ForeignKey(User, related_name="hr_interviewer_user", null=True, blank=True,
                                            on_delete=models.CASCADE, verbose_name="HR面试官")
    hr_remark = models.CharField(max_length=256, blank=True, verbose_name="HR复试备注")

    creator = models.CharField(max_length=256, blank=True, verbose_name="候选人数据创建者")
    created_date = models.DateTimeField(auto_now=True, verbose_name="创建时间")
    modified_date = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="更新时间")
    last_editor = models.CharField(max_length=256, blank=True, verbose_name="最后编辑者")

    # 设置字段样式
    def color_first_result(self):
        color_code = 'black'
        if self.first_result == '建议复试':
            color_code = 'green'
        elif self.first_result == '待定':
            color_code = 'blue'
        elif self.first_result == '放弃':
            color_code = 'red'
        return format_html('<span style="color:{};">{}</span>'.format(color_code, self.first_result))

    color_first_result.short_description = '一轮面试结果'

    def color_second_result(self):
        color_code = 'black'
        if self.second_result == '建议复试':
            color_code = 'green'
        elif self.second_result == '待定':
            color_code = 'blue'
        elif self.second_result == '放弃':
            color_code = 'red'
        return format_html('<span style="color:{};">{}</span>'.format(color_code, self.second_result))

    color_second_result.short_description = '专业复试结果'

    def color_hr_result(self):
        color_code = 'black'
        if self.hr_result == '建议录用':
            color_code = 'green'
        elif self.hr_result == '待定':
            color_code = 'blue'
        elif self.hr_result == '放弃':
            color_code = 'red'
        return format_html('<span style="color:{};">{}</span>'.format(color_code, self.hr_result))

    color_hr_result.short_description = 'HR复试结果'

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'candidate'
        verbose_name = '应聘者'
        verbose_name_plural = '应聘者'
        permissions = [
            ("export", "Can export 应聘者 list"),
            ("notify", "Can notify interviewer for candidate review")
        ]
