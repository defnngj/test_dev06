<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="800px"
    :before-close="closeDialog"
  >
    <el-table
      class="edit-case"
      :data="tableData"
      border
      row-key="id"
      align="left"
      height="250"
    >
      <el-table-column
        v-for="(item, index) in col"
        :key="`col_${index}`"
        :prop="dropCol[index].prop"
        :label="item.label"
      >
      </el-table-column>
    </el-table>
    <div style="margin-top: 20px; text-align: right">
      <el-button
        type="primary"
        size="small"
        @click="saveCaseList()"
        style="margin-bottom: 20px"
        >保存</el-button
      >
    </div>
  </el-dialog>
</template>

<script>
import TaskApi from "../../request/task"
import Sortable from "sortablejs"

export default {
  name: "Dialog",
  props: ["pid", "tid"],
  components: {},
  data() {
    return {
      showTitle: "",
      dialogVisible: true,
      col: [
        {
          label: "ID",
          prop: "id",
        },
        {
          label: "名称",
          prop: "name",
        },
        {
          label: "方法",
          prop: "method",
        },
        {
          label: "地址",
          prop: "url",
        },
      ],
      dropCol: [
        {
          label: "ID",
          prop: "id",
        },
        {
          label: "名称",
          prop: "name",
        },
        {
          label: "方法",
          prop: "method",
        },
        {
          label: "地址",
          prop: "url",
        },
      ],
      tableData: [],
    }
  },
  created() {
    this.showTitle = "调整用例顺序"
    this.initCaesList()
  },
  mounted() {
    this.$nextTick(() => {
      this.rowDrop()
      this.columnDrop()
    })
  },
  methods: {
    closeDialog() {
      this.$emit("cancel", {})
    },

    // 查询任务用例列表
    async initCaesList() {
      const resp = await TaskApi.getTaskCaseList(this.tid)
      if (resp.success === true) {
        this.tableData = resp.items
      } else {
        this.$message.error("查询失败！")
      }
    },

    //行拖拽
    rowDrop() {
      const tbody = document.querySelectorAll(
        ".el-table__body-wrapper tbody"
      )[1]
      const _this = this
      Sortable.create(tbody, {
        onEnd({ newIndex, oldIndex }) {
          console.log("拖动了行", "当前序号: " + newIndex)
          const currRow = _this.tableData.splice(oldIndex, 1)[0]
          _this.tableData.splice(newIndex, 0, currRow)
        },
      })
    },
    //列拖拽
    columnDrop() {
      const wrapperTr = document.querySelectorAll(
        ".el-table__header-wrapper tr"
      )[1]
      this.sortable = Sortable.create(wrapperTr, {
        animation: 180,
        delay: 0,
        onEnd: (evt) => {
          console.log("拖动了列")
          const oldItem = this.dropCol[evt.oldIndex]
          this.dropCol.splice(evt.oldIndex, 1)
          this.dropCol.splice(evt.newIndex, 0, oldItem)
        },
      })
    },

    // 保存用例列表
    async saveCaseList() {
      console.log("tableData-->", this.tableData)
      var caseList = []
      for (let i = 0; i < this.tableData.length; i++) {
        console.log(this.tableData[i].id)
        caseList.push(this.tableData[i].id)
      }
      console.log(caseList)
      var req = { caseList: caseList }
      const resp = await TaskApi.updataTaskCaseList(this.tid, req)
      if (resp.success === true) {
        // this.tableData = resp.items
        this.$message.success("保存成功")
        this.closeDialog()
      } else {
        this.$message.error("查询失败！")
      }
    },
  },
}
</script>
<style scoped>
#image {
  text-align: left;
}
</style>
