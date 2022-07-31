<template>
  <div class="home">
    <div>
      <div>监控页面</div>
      <div style="margin-bottom: 10px; text-align: left">
        <el-button type="primary" @click="startMonitoring">开始监控</el-button>
        <el-button
          @click="showLoading()"
          type="primary"
          style="margin-left: 16px"
          >接口压测</el-button
        >
      </div>

      <div
        id="cpuChart"
        :style="{ width: '380px', height: '380px' }"
        style="margin: 0 auto; float: left"
      ></div>

      <div
        id="memoryChart"
        :style="{ width: '380px', height: '380px' }"
        style="margin: 0 auto; float: right"
      ></div>
    </div>

    <el-drawer
      title="压测接口"
      :visible.sync="drawer"
      :direction="direction"
      :before-close="handleClose"
    >
      <span>
        <el-form ref="form" :model="form" label-width="80px">
          <el-form-item label="项目">
            <el-select
              v-model="form.project"
              placeholder="请选择项目"
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
          </el-form-item>
          <el-form-item label="接口">
            <el-select
              v-model="form.interface"
              filterable
              placeholder="请选择接口"
              @change="changeInterface"
            >
              <el-option
                v-for="item in interfaceOption"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              >
              </el-option>
            </el-select>
            <el-descriptions title="接口信息" border :column="1">
              <el-descriptions-item label="名称">{{
                api.name
              }}</el-descriptions-item>
              <el-descriptions-item label="URL">{{
                api.url
              }}</el-descriptions-item>
              <el-descriptions-item label="方法">{{
                api.method
              }}</el-descriptions-item>
            </el-descriptions>
          </el-form-item>
          <el-form-item label="压测参数">
            <el-col :span="11">
              <el-input-number
                v-model="loadForm.user"
                :min="1"
                :max="10"
                label="用户数"
                size="mini"
              ></el-input-number>
            </el-col>
            <el-col class="line" :span="2">-</el-col>
            <el-col :span="11">
              <el-input-number
                v-model="loadForm.request"
                :min="1"
                :max="10"
                label="请求数"
                size="mini"
              ></el-input-number>
            </el-col>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="startLoading">开始压测</el-button>
            <el-button>取消</el-button>
          </el-form-item>
        </el-form>
      </span>
    </el-drawer>
  </div>
</template>

<script>
// @ is an alias to /src
import * as echarts from "echarts"
import ProjectApi from "../../request/project"
import PerformanceApi from "../../request/performance"

export default {
  name: "Porject",
  components: {
    //组件
  },
  data() {
    return {
      cpuSocket: "",
      memorySocket: "",
      textarea: "",
      input: "start monitoring",
      drawer: false,
      direction: "rtl",
      form: {
        project: "",
        interface: "",
      },
      loadForm: {
        id: "",
        user: 1,
        request: 1,
      },
      projectOption: [],
      interfaceData: [],
      interfaceOption: [],
      api: {
        name: "",
        url: "",
        mehtod: "",
      },
      cpuChart: "",
      cpuChartOption: {
        color: ["#42d29d"],
        title: {},
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "cross",
            label: {
              backgroundColor: "#fa6767",
            },
          },
        },
        legend: {
          data: ["cpu"],
        },
        toolbox: {
          feature: {
            saveAsImage: {},
          },
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true,
        },
        xAxis: {
          type: "category",
          boundaryGap: false,
          data: [],
        },
        yAxis: {
          type: "value",
        },
        series: [
          {
            name: "cpu",
            type: "line",
            areaStyle: {},
            data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          },
        ],
      },
      memoryChartOption: {
        title: {
          // text: 'Memory utilization'
        },
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "cross",
            label: {
              backgroundColor: "#fa6767",
            },
          },
        },
        legend: {
          data: ["memory"],
        },
        toolbox: {
          feature: {
            saveAsImage: {},
          },
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true,
        },
        xAxis: {
          type: "category",
          boundaryGap: false,
          data: [],
        },
        yAxis: {
          type: "value",
        },
        series: [
          {
            name: "memory",
            type: "line",
            areaStyle: {},
            data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          },
        ],
      },

      ctime: ["", "", "", "", "", "", "", "", "", ""],
      cpu: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      mtime: ["", "", "", "", "", "", "", "", "", ""],
      memory: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    }
  },

  created() {
    this.initConn()
  },

  mounted() {
    this.$nextTick(() => {
      this.initEChart()
    })
  },

  methods: {
    // 初始化项目列表
    async initProjectList() {
      this.projectOption = []
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
        this.$message.success("查询成功！")
      } else {
        this.$message.error("查询失败！")
      }
    },
    // 修改选中项目
    async changeProject(value) {
      console.log("value", value)
      const resp = await ProjectApi.getProjectCases(value)
      if (resp.success === true) {
        this.interfaceData = resp.items
        for (let i = 0; i < resp.items.length; i++) {
          this.interfaceOption.push({
            value: resp.items[i].id,
            label: resp.items[i].name,
          })
        }
        this.$message.success("查询成功！")
      } else {
        this.$message.error("查询失败！")
      }
    },
    async changeInterface(value) {
      for (let i = 0; i < this.interfaceData.length; i++) {
        if (value == this.interfaceData[i].id) {
          this.loadForm.id = value
          this.api = this.interfaceData[i]
        }
      }
    },

    // 初始化图表
    async initEChart() {
      this.cpuChart = echarts.init(document.getElementById("cpuChart"))
      this.cpuChart.setOption(this.cpuChartOption)
      this.memoryChart = echarts.init(document.getElementById("memoryChart"))
      this.memoryChart.setOption(this.memoryChartOption)
    },

    updateCpuChart(res) {
      // 准备数据
      this.ctime.push(res.data[0])
      this.cpu.push(parseFloat(res.data[1]))
      if (this.ctime.length >= 10) {
        this.ctime.shift()
        this.cpu.shift()
      }
      // 填入数据
      this.cpuChart.setOption({
        xAxis: {
          data: this.ctime,
        },
        series: [
          {
            name: "cpu",
            data: this.cpu,
          },
        ],
      })
    },

    updateMemoryChart(res) {
      // 准备数据
      this.mtime.push(res.data[0])
      this.memory.push(parseFloat(res.data[1]))
      if (this.mtime.length >= 10) {
        this.mtime.shift()
        this.memory.shift()
      }
      // 填入数据
      this.memoryChart.setOption({
        xAxis: {
          data: this.mtime,
        },
        series: [
          {
            name: "memory",
            data: this.memory,
          },
        ],
      })
    },

    // 初始化websokit连接
    initConn() {
      const wss_protocol =
        window.location.protocol == "https:" ? "wss://" : "ws://"
      this.cpuSocket = new WebSocket(
        wss_protocol + "127.0.0.1:8000/ws/performance/cpu/"
      )
      this.cpuSocket.onopen = this.onOpen
      this.cpuSocket.onmessage = this.onMessage
      this.cpuSocket.onclose = this.onClose

      this.memorySocket = new WebSocket(
        wss_protocol + "127.0.0.1:8000/ws/performance/memory/"
      )
      this.memorySocket.onopen = this.onOpen2
      this.memorySocket.onmessage = this.onMessage2
      this.memorySocket.onclose = this.onClose2
    },

    onOpen() {
      this.textarea +=
        this.textarea + "[公告]欢迎来到vue.js讨论群。请文明发言!\n"
    },
    onOpen2() {
      this.textarea +=
        this.textarea + "[公告]欢迎来到vue.js讨论群。请文明发言!\n"
    },

    onMessage(e) {
      console.log("on-msg", e)
      const data = JSON.parse(e.data)
      console.log("cpu msg-->", data.message)
      this.updateCpuChart(data.message)
    },
    onMessage2(e) {
      console.log("on-msg", e)
      const data = JSON.parse(e.data)
      console.log("memery msg-->", data.message)
      this.updateMemoryChart(data.message)
    },

    onClose(e) {
      console.error("e", e)
    },

    onClose2(e) {
      console.error("e", e)
    },

    startMonitoring() {
      this.textarea += "开始性能"
      this.cpuSocket.send(
        JSON.stringify({
          message: this.input,
        })
      )
      // this.memorySocket.send(
      //   JSON.stringify({
      //     message: this.input,
      //   })
      // )
    },

    // 接口压测按钮
    showLoading() {
      console.log("显示抽屉")
      this.drawer = true
      this.initProjectList()
    },
    async startLoading() {
      const resp = await PerformanceApi.LoadingCase(this.loadForm)
      if (resp.success === true) {
        this.$message.success("开始压测！")
      } else {
        this.$message.error("压测失败！")
      }
    },

    handleClose() {
      this.drawer = false
    },
  },
}
</script>
