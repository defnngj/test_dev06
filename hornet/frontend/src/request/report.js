import request from "@/HttpCommon.js"

class ReportApi {

  getReportList(data) {
    return request.get("/api/reports/list", data)
  }

  getReportDetail(rid) {
    return request.get("/api/reports/" + rid + "/")
  }

  deleteReport(rid) {
    return request.delete("/api/reports/" + rid + "/")
  }
}

export default new ReportApi()
