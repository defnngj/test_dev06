<template>
  <div class="case">
    <div style="height: 50px">
      <span style="float: left">
        <p>项目:</p>
      </span>
      <span style="float: left">
        <el-select
          v-model="projectValue"
          placeholder="请选择项目"
          size="medium"
          @change="changeProject"
        >
          <el-option
            v-for="item in projectOption"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
      </span>
      <span>
        <el-button @click="createCase()" type="primary" size="medium"
          >创建</el-button
        >
      </span>
    </div>
    <div style="margin-top: 10px">
      <el-card style="width: 28%; float: left">
        <el-button
          type="text"
          icon="el-icon-circle-plus-outline"
          @click="createRootModule"
          >根节点</el-button
        >
        <el-tree
          :data="moduleData"
          show-checkbox
          node-key="id"
          default-expand-all
          :expand-on-click-node="false"
          @node-click="nodeClick"
        >
          <span class="custom-tree-node" slot-scope="{ node, data }">
            <span>{{ node.label }}</span>
            <span>
              <el-button type="text" size="mini" @click="() => append(data)">
                <i class="el-icon-circle-plus-outline"></i>
              </el-button>
              <el-button
                type="text"
                size="mini"
                @click="() => remove(node, data)"
              >
                <i class="el-icon-delete"></i>
              </el-button>
            </span>
          </span>
        </el-tree>
      </el-card>
      <div style="width: 70%; float: right">
        <el-table
          :data="casesData"
          border
          style="width: 100%"
          @row-click="caseRowClick"
        >
          <el-table-column prop="id" label="ID" width="50"> </el-table-column>
          <el-table-column prop="name" label="名称" width="180">
          </el-table-column>
          <el-table-column prop="method" label="方法" width="80">
          </el-table-column>
          <el-table-column prop="url" label="URL" width="180">
          </el-table-column>
          <el-table-column prop="module.name" label="模块" width="100">
          </el-table-column>
          <el-table-column prop="create_time" label="创建时间">
          </el-table-column>
        </el-table>
      </div>

      <el-drawer
        :title="caseTitle"
        :visible.sync="drawer"
        direction="ltr"
        :before-close="handleClose"
        size="50%"
      >
        <CaseDialog v-if="drawer"></CaseDialog>
      </el-drawer>
    </div>

    <!-- 创建模块 -->
    <moduleDialog
      v-if="dialogFlag"
      :projectId="projectValue"
      :projectLabel="projectLabel"
      :rootId="rootFlag"
      :parentObj="parentObj"
      @cancel="closeDialog"
    >
    </moduleDialog>
  </div>
</template>

<script>
import ProjectApi from "../../request/project"
import ModuleApi from "../../request/module"
import moduleDialog from "./moduleDialog.vue"
import CaseDialog from "./CaseDialog.vue"

export default {
  name: "HelloWorld",
  components: {
    moduleDialog,
    CaseDialog,
  },
  data() {
    return {
      projectValue: 1,
      projectLabel: "",
      rootFlag: true,
      projectOption: [],
      moduleData: [],
      dialogFlag: false,
      parentObj: {},
      casesData: [],
      drawer: false,
      caseTitle: "",
    }
  },
  mounted() {
    console.log("mounted11")
    this.initProjectList()
    this.initModuleList(this.projectValue)
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

        // this.$message.success("查询成功！")
      } else {
        this.$message.error("查询失败！")
      }
    },

    // 修改选中项目
    changeProject(value) {
      console.log("change project -->", value)
      this.projectValue = value
      this.projectLabel = this.projectOption.find(
        (item) => item.value === value
      ).label
      console.log("选择项目名称", this.projectLabel)
      this.initModuleList(value)
    },

    // 查询模块列表
    async initModuleList(pid) {
      const req = { project_id: pid }
      const resp = await ModuleApi.getModuleTree(req)
      if (resp.success === true) {
        console.log("module list -->", resp.items)
        this.moduleData = resp.items
        // this.$message.success("查询成功！")
      } else {
        this.$message.error("查询失败！")
      }
    },

    append(data) {
      console.log("创建子节点", data.label)
      this.dialogFlag = true
      this.rootFlag = false
      this.parentObj = data
    },

    remove(node, data) {
      console.log("删除节点", data)
      ModuleApi.deleteModule(data.id).then((resp) => {
        if (resp.success === true) {
          this.$message.success("删除成功！")
          this.initModuleList(this.projectValue)
        } else {
          this.$message.error(resp.error.msg)
        }
      })
    },

    // 创建根节点
    createRootModule() {
      this.dialogFlag = true
      this.rootFlag = true
    },

    // 创建模块关闭
    closeDialog() {
      this.dialogFlag = false
      this.parentObj = {}
      this.initModuleList(this.projectValue)
    },

    nodeClick(data) {
      console.log("点击节点", data)
      this.getCaseList(data.id)
    },

    async getCaseList(mid) {
      const resp = await ModuleApi.getModuleCase(mid)
      if (resp.success === true) {
        this.casesData = resp.items
        this.$message.success("查询成功！")
      } else {
        this.$message.error("查询失败！")
      }
    },

    createCase() {
      ;(this.drawer = true), (this.caseTitle = "创建用例")
    },

    caseRowClick(row) {
      console.log("点击用例", row)
      this.drawer = true
      this.caseTitle = "查看用例"
    },
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
