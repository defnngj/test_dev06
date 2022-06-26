<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="1000px"
    :before-close="closeDialog"
  >
    <el-form
      :model="taskForm"
      :rules="rules"
      ref="ruleForm"
      label-width="100px"
      class="demo-ruleForm"
    >
      <el-form-item label="统计">
        <div id="youChart" :style="{width: '380px', height: '380px'}" style="margin: 0 auto;"></div>
        <el-table
          :data="reportData"
          border
          style="width: 100%">
          <el-table-column prop="name" label="名称"> </el-table-column>
          <el-table-column prop="tests" label="总数"> </el-table-column>
          <el-table-column prop="passed" label="通过"> </el-table-column>
          <el-table-column prop="failure" label="失败"> </el-table-column>
          <el-table-column prop="error" label="错误"> </el-table-column>
          <el-table-column prop="skipped" label="跳过"> </el-table-column>
          <el-table-column prop="run_time" label="时长"> </el-table-column>
          <el-table-column prop="create_time" label="创建时间"> </el-table-column>
        </el-table>
      </el-form-item>
      <el-form-item label="详细日志">
        <el-input type="textarea" :rows="10" v-model="detailLog"></el-input>
      </el-form-item>

      <el-form-item style="text-align: right">
        <div class="dialog-footer">
          <el-button @click="closeDialog()">取消</el-button>
          <el-button type="primary" @click="submitForm('ruleForm')"
            >保存</el-button
          >
        </div>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script>
import TaskApi from "../../request/task"
import ReportApi from "../../request/report"
import * as echarts from "echarts"

export default {
  name: "Dialog",
  props: ["rid"],
  components: {},
  data() {
    return {
      showTitle: "查看报告",
      dialogVisible: true,
      detailLog: '',
      reportData: [],
      chartOption: {
        tooltip: {
          trigger: "item",
        },
        legend: {
          top: "5%",
          left: "center",
        },
        series: [
          {
            name: "比例",
            type: "pie",
            radius: "50%",
            data: [
              { value: 1, name: "跳过" },
              { value: 10, name: "通过" },
              { value: 3, name: "失败" },
              { value: 2, name: "错误" },
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)",
              },
            },
          },
        ],
      },
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initEChart()
    })
  },

  methods: {
    closeDialog() {
      this.$emit("cancel", {})
    },

    // 初始化图表
    async initEChart() {
      var myChart = echarts.init(document.getElementById("youChart"))
      const resp = await ReportApi.getReportDetail(this.rid)
      this.chartOption.series[0].data = []
      if (resp.success === true) {
        console.log("resp--->", resp.item)
        console.log("option--->", this.chartOption.series[0].data)
        this.reportData.push(resp.item) 
        this.chartOption.series[0].data.push({ value: resp.item.skipped, name: "跳过" })
        this.chartOption.series[0].data.push({ value: resp.item.passed, name: "通过" })
        this.chartOption.series[0].data.push({ value: resp.item.failure, name: "失败" })
        this.chartOption.series[0].data.push({ value: resp.item.error, name: "错误" })
        this.detailLog = resp.item.result
        // this.reportData = resp.item
        // this.$message.success("查询成功！")
      } else {
        this.$message.error("查询失败！")
      }
      myChart.setOption(this.chartOption)
    },

    // 创建项目
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          if (this.title == "create") {
            TaskApi.createTask(this.taskForm).then((resp) => {
              if (resp.success === true) {
                this.closeDialog()
                this.$message.success("创建成功！")
              } else {
                this.$message.error(resp.error.message)
              }
            })
          } else if (this.title == "edit") {
            TaskApi.updateTask(this.tid, this.taskForm).then((resp) => {
              if (resp.success === true) {
                this.closeDialog()
                this.$message.success("更新成功！")
              } else {
                this.$message.error(resp.error.message)
              }
            })
          }
        } else {
          return false
        }
      })
    },
  },
}
</script>
<style scoped>
#image {
  text-align: left;
}
</style>
