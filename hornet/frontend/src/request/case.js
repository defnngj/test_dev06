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

  updateCase(cid, data) {
    return request.put("/api/cases/" + cid + "/", data)
  }

  getCase(cid) {
    return request.get("/api/cases/" + cid + "/")
  }

  checkExtract(data) {
    return request.post("/api/cases/extract", data)
  }
}

export default new CaseApi()
