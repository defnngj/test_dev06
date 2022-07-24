<template>
  <div class="home">
    <div>
      <div>监控页面</div>
      <div style="margin-bottom: 10px; text-align: left">
        <el-button type="primary" @click="onSubmit">开始监控</el-button>
      </div>
      <div
        id="youChart"
        :style="{ width: '380px', height: '380px' }"
        style="margin: 0 auto"
      ></div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import * as echarts from "echarts"

export default {
  name: "Porject",
  components: {
    //组件
  },
  data() {
    return {
      socket: "",
      textarea: "",
      input: "",
      myChart: "",
      chartOption: {
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
      ctime: ["", "", "", "", "", "", "", "", "", ""],
      cpu: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
    // 初始化图表
    async initEChart() {
      this.myChart = echarts.init(document.getElementById("youChart"))
      this.myChart.setOption(this.chartOption)
    },

    updateChart(res) {
      // 准备数据
      this.ctime.push(res.data[0])
      this.cpu.push(parseFloat(res.data[1]))
      if (this.ctime.length >= 10) {
        this.ctime.shift()
        this.cpu.shift()
      }
      // 填入数据
      this.myChart.setOption({
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

    // 初始化websokit连接
    initConn() {
      const wss_protocol =
        window.location.protocol == "https:" ? "wss://" : "ws://"
      // this.socket = new WebSocket(
      //   wss_protocol + window.location.host + "/ws/performance/chat/"
      // )
      this.socket = new WebSocket(
        wss_protocol + "127.0.0.1:8000/ws/performance/cpu/"
      )
      this.socket.onopen = this.onOpen
      this.socket.onmessage = this.onMessage
      this.socket.onclose = this.onClose
    },

    onOpen() {
      this.textarea +=
        this.textarea + "[公告]欢迎来到vue.js讨论群。请文明发言!\n"
      // let mes = {}
      // mes.type = "test"
      // this.socket.send(JSON.stringify(mes))
    },

    onMessage(e) {
      console.log("on-msg", e)
      const data = JSON.parse(e.data)
      console.log("data-->", data.message)
      this.updateChart(data.message)
    },

    onClose(e) {
      console.error("e", e)
    },

    onSubmit() {
      this.textarea += "开始性能"
      this.socket.send(
        JSON.stringify({
          message: this.input,
        })
      )
    },
  },
}
</script>
