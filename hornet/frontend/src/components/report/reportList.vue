<template>
  <div class="home">
    <div style="text-align: left">
      <el-form :inline="true" :model="projectForm">
        <el-form-item label="项目">
          <el-select
            v-model="projectForm.id"
            size="medium"
            placeholder="请选择项目"
          >
            <el-option
              v-for="item in projectOption"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
    </div>

    <div>
      <el-table :data="reportData" border style="width: 100%">
        <el-table-column prop="id" label="ID"> </el-table-column>
        <el-table-column prop="name" label="名称"> </el-table-column>
        <el-table-column prop="tests" label="总数"> </el-table-column>
        <el-table-column prop="passed" label="通过">
          <template slot-scope="scope">
            <el-tag type="success"> {{ scope.row.passed }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="error" label="错误">
          <template slot-scope="scope">
            <el-tag type="danger"> {{ scope.row.error }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="failure" label="失败">
          <template slot-scope="scope">
            <el-tag type="warning"> {{ scope.row.failure }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="skipped" label="跳过">
          <template slot-scope="scope">
            <el-tag type="info"> {{ scope.row.skipped }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="run_time" label="时长"> </el-table-column>
        <el-table-column prop="create_time" label="创建"> </el-table-column>
        <el-table-column fixed="right" label="操作" width="150">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="showReport(scope.row)"
              >查看</el-button
            >
            <el-button type="text" size="small" @click="deleteReport(scope.row)"
              >删除</el-button
            >
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div style="width: 100%; text-align: right">
      <el-pagination
        background
        @current-change="handleCurrentChange"
        layout="prev, pager, next"
        :page-size="req.size"
        :total="total"
      >
      </el-pagination>
    </div>

    <!-- 引入子组件 -->
    <reportDialog
      v-if="dialogFlag"
      :rid="reportId"
      @cancel="closeDialog"
    ></reportDialog>
  </div>
</template>

<script>
// @ is an alias to /src
import reportDialog from "@/components/report/reportDialog.vue"
import ProjectApi from "../../request/project"
import ReportApi from "../../request/report"

export default {
  name: "Porject",
  components: {
    reportDialog,
  },
  data() {
    return {
      projectForm: {
        id: 1,
      },
      projectOption: [],
      dialogFlag: false,
      currentPorjectId: "",
      reportId: "",
      projectData: [],
      req: {
        page: 1,
        size: 6,
      },
      total: 50,
      reportData: [],
      taskHeartbeat: null,
    }
  },
  mounted() {
    this.initProjectList()
  },
  methods: {
    // 初始化项目列表
    async initProjectList() {
      const resp = await ProjectApi.getProjects(this.req)
      if (resp.success === true) {
        this.projectValue = resp.items[0].id
        this.projectLabel = resp.items[0].name

        for (let i = 0; i < resp.items.length; i++) {
          this.projectOption.push({
            value: resp.items[i].id,
            label: resp.items[i].name,
          })
        }
        this.initReportList()
        // this.$message.success("查询成功！")
      } else {
        this.$message.error("查询失败！")
      }
    },
    // 初始化报告列表
    async initReportList() {
      const req = { project_id: this.projectForm.id }
      const resp = await ReportApi.getReportList(req)
      if (resp.success === true) {
        this.reportData = resp.items
        // this.$message.success("查询成功！")
      } else {
        this.$message.error("查询失败！")
      }
    },

    showReport(row) {
      this.reportId = row.id
      this.dialogFlag = true
    },

    closeDialog() {
      this.dialogFlag = false
      // this.initProjectList()
    },

    // 跳转到第几页
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`)
      this.req.page = val
      this.initProjectList()
    },

    // 删除报告
    async deleteReport(row) {
      const resp = await ReportApi.deleteReport(row.id)
      if (resp.success === true) {
        this.initProjectList()
        this.$message.success("删除成功！")
      } else {
        this.$message.error("删除失败！")
      }
    },
  },
}
</script>
