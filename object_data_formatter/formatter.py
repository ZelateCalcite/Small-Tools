"""
example input
<el-row>
        <el-col :span="8">
          <el-form-item label="客户名称" prop="">
            <el-input v-model="auditForm" placeholder="请输入"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="协议类型" prop="agreementType">
            <dict-select :show-all="false" v-model="auditForm.agreementType" placeholder="请选择" dict-key="agreementType"></dict-select>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="所属行业" prop="beltoIndu">
            <dict-select :show-all="false" v-model="auditForm.beltoIndu" placeholder="请选择" dict-key="beltoInduType"></dict-select>
          </el-form-item>
        </el-col>
      </el-row>
"""

import re


def vue_model_extractor(form_name: str, html_data: str, label_name: str, ) -> [str]:
    # eg. form_name: auditForm
    # eg. html_data: <tag v-model="auditForm.props">
    # eg. label_name: <tag label="some label">
    pattern_model = re.compile(form_name + r'\.[A-Za-z]+')
    pattern_label = re.compile(label_name + r'=\"[\u4e00-\u9fa5]*\"?')
    definition = re.findall(pattern_model, html_data)
    comment = re.findall(pattern_label, html_data)
    for i in range(len(definition)):
        definition[i] = definition[i].split(i)[1]
        comment[i] = comment[i].split('"')[-1]
    return [(definition[i], comment[i]) for i in range(len(definition))]


def print_data_object(properties: [str], comments: [str]) -> None:
    for i in range(len(properties)):
        print(properties[i] + ": '', // " + comments[i])

