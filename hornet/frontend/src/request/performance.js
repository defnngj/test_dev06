import request from "@/HttpCommon.js"

class PerformanceApi {
  LoadingCase(data) {
    return request.post("/api/performance/loading", data)
  }
}

export default new PerformanceApi()
