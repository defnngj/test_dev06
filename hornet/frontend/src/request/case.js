import request from "@/HttpCommon.js"

class CaseApi {
  debugCase(data) {
    return request.post("/api/cases/debug", data)
  }

  assertCase(data) {
    return request.post("/api/cases/assert", data)
  }

  createCase(data) {
    return request.post("/api/cases/", data)
  }

  getCase(cid) {
    return request.get("/api/cases/" + cid + "/")
  }
}

export default new CaseApi()
