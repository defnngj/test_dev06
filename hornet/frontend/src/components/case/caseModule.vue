<template>
  <div class="case">
    <div style="height: 50px">
      <span style="float: left">
        <p>项目:</p>
      </span>
      <span>
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
    </div>
    <div style="margin-top: 10px">
      <el-card style="width: 300px">
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
    </div>

    <!-- 创建模块 -->
    <moduleDialog
      v-if="dialogFlag"
      :pid="projectValue"
      :plabel="projectLabel"
      :rootId="rootFlag"
      @cancel="closeDialog"
    >
    </moduleDialog>
  </div>
</template>

<script>
import ProjectApi from "../../request/project"
import ModuleApi from "../../request/module"
import moduleDialog from "./moduleDialog.vue"

export default {
  name: "HelloWorld",
  components: {
    moduleDialog,
  },
  data() {
    return {
      projectValue: 1,
      projectLabel: "",
      rootFlag: true,
      projectOption: [],
      moduleData: [],
      dialogFlag: false,
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
      console.log("创建子节点", data)
      // console.log("data", data)
      // const newChild = { id: id++, label: "testtest", children: [] }
      // if (!data.children) {
      //   this.$set(data, "children", [])
      // }
      // data.children.push(newChild)
    },

    remove(node, data) {
      console.log("删除节点", node, data)
      // const parent = node.parent
      // const children = parent.data.children || parent.data
      // const index = children.findIndex((d) => d.id === data.id)
      // children.splice(index, 1)
    },

    // 创建模块
    createRootModule() {
      this.dialogFlag = true
      this.rootFlag = true
    },

    // 创建模块关闭
    closeDialog() {
      this.dialogFlag = false
      this.initModuleList(this.projectValue)
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
