import request from "@/HttpCommon.js"

class CaseApi {

  debugCase(data) {
    return request.post("/api/cases/debug", data)
  }

}

export default new CaseApi()
