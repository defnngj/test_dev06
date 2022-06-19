<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="800px"
    :before-close="closeDialog"
  >
    <el-form
      :model="taskForm"
      :rules="rules"
      ref="ruleForm"
      label-width="100px"
      class="demo-ruleForm"
    >
      <el-form-item label="名称" prop="name">
        <el-input v-model="taskForm.name"></el-input>
      </el-form-item>
      <el-form-item label="描述">
        <el-input type="textarea" v-model="taskForm.describe"></el-input>
      </el-form-item>
      <el-form-item>
        <div style="margin-top: 10px">
          <el-card style="width: 28%; float: left">
            <el-tree
              :data="moduleData"
              node-key="id"
              default-expand-all
              :expand-on-click-node="false"
              @node-click="nodeClick"
            >
              <span class="custom-tree-node" slot-scope="{ node }">
                <span style="float: left">{{ node.label }}</span>
              </span>
            </el-tree>
          </el-card>
          <div style="width: 70%; float: right">
            <el-table
              ref="multipleTable"
              :data="casesData"
              border
              style="width: 100%"
              @select="selectionOneCase"
              @select-all="selectionAllCases"
            >
              <el-table-column type="selection" width="55"> </el-table-column>
              <el-table-column prop="id" label="ID" width="50">
              </el-table-column>
              <el-table-column prop="name" label="名称"> </el-table-column>
            </el-table>
          </div>
        </div>
      </el-form-item>
      <el-form-item style="text-align: right">
        <div class="dialog-footer">
          已选择【{{ this.caseNum }}】条用例
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
import ProjectApi from "../../request/project"
import ModuleApi from "../../request/module"
import TaskApi from "../../request/task"

export default {
  name: "Dialog",
  props: ["title", "pid", "tid"],
  components: {},
  data() {
    return {
      showTitle: "",
      dialogVisible: true,
      taskForm: {
        project: 0,
        name: "",
        describe: "",
        cases: [],
      },
      rules: {
        name: [
          { required: true, message: "请输入任务的名称", trigger: "blur" },
        ],
      },
      moduleData: [],
      casesData: [],
      currentModuleId: 0,
      caseNum: 0,
    }
  },
  mounted() {
    this.taskForm.project = this.pid
    if (this.title == "create") {
      this.showTitle = "创建任务"
    } else if (this.title == "edit") {
      this.showTitle = "编辑任务"
    }
    this.initModuleList()
  },

  methods: {
    closeDialog() {
      this.$emit("cancel", {})
    },

    // 查询模块列表
    async initModuleList() {
      const req = { project_id: this.pid }
      const resp = await ModuleApi.getModuleTree(req)
      if (resp.success === true) {
        this.moduleData = resp.items
        if (this.title == "edit") {
          this.initTaskInfo()
        }
      } else {
        this.$message.error("查询失败！")
      }
    },

    // 查询任务详情
    async initTaskInfo() {
      const resp = await TaskApi.getTaskDetail(this.tid)
      if (resp.success === true) {
        this.taskForm = resp.item
        this.calculationCase()
      } else {
        this.$message.error("查询失败！")
      }
    },

    // 点击模块
    nodeClick(data) {
      this.currentModuleId = data.id
      this.getModuleCaseList(data.id)
    },

    // 选择所有用例
    selectionAllCases(val) {
      console.log("选择所有用例", val)
      this.selectiveCase(val)
    },

    // 选择一条用例
    selectionOneCase(val, row) {
      console.log("selection-one-change", val)
      console.log("selection-one-change", row)
      this.selectiveCase(val)
    },

    // 公共方法：选择用例
    selectiveCase(multipleSelection) {
      const moduleCases = []
      for (let i = 0; i < multipleSelection.length; i++) {
        moduleCases.push(multipleSelection[i].id)
      }

      var selective = false
      for (let i = 0; i < this.taskForm.cases.length; i++) {
        if (this.taskForm.cases[i].moduleId == this.currentModuleId) {
          selective = true
          this.taskForm.cases[i].casesId = moduleCases
        }
      }
      if (selective == false) {
        this.taskForm.cases.push({
          moduleId: this.currentModuleId,
          casesId: moduleCases,
        })
      }
      this.calculationCase()
    },

    // 初始化用例数据
    async getModuleCaseList(mid) {
      const resp = await ModuleApi.getModuleCase(mid)
      if (resp.success == true) {
        this.casesData = resp.items
        // this.$message.success("查询成功！")

        // 已经选中的用例
        this.$nextTick(() => {
          var casesId = []
          for (let i = 0; i < this.taskForm.cases.length; i++) {
            if (this.taskForm.cases[i].moduleId == mid) {
              casesId = this.taskForm.cases[i].casesId
            }
          }

          let rows = []
          for (let i = 0; i < casesId.length; i++) {
            for (let j = 0; j < this.casesData.length; j++) {
              if (casesId[i] == this.casesData[j].id) {
                rows.push(this.casesData[j])
              }
            }
          }
          rows.forEach((row) => {
            this.$refs.multipleTable.toggleRowSelection(row)
          })
        })
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 公共方法：计算用例数量
    calculationCase() {
      this.caseNum = 0
      for (let i = 0; i < this.taskForm.cases.length; i++) {
        this.caseNum += this.taskForm.cases[i].casesId.length
      }
    },

    // 项目详情
    async initProject() {
      const resp = await ProjectApi.getProject(this.pid)
      if (resp.success === true) {
        this.taskForm = resp.item
        this.fileList.push({
          name: resp.item.image,
          url: "static/images/" + resp.item.image,
        })
        this.$message.success("项目详情成功！")
      } else {
        this.$message.error("项目详情失败！")
      }
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
