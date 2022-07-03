// https://docs.cypress.io/api/introduction/api.html

describe("test project manage", () => {
  it("create", () => {
    cy.visit("#/main/project")
    // cy.contains("h2", "接口测试平台")
    var timestamp = Date.parse(new Date())
    cy.get("[cy-data=ProjectCreate]", { timeout: 3000 }).click()
    cy.get("[cy-data=ProjectName]", { timeout: 3000 }).type(
      "项目" + timestamp.toString()
    )
    cy.get("[cy-data=ProjectDescribe]", { timeout: 3000 }).type("项目描述")
    cy.get("[cy-data=ProjectOK]", { timeout: 3000 }).click()
  })
  it("edit", () => {
    cy.visit("#/main/project")
    // cy.contains("h2", "接口测试平台")
    var timestamp = Date.parse(new Date())
    cy.get("[cy-data=ProjectSetting]", { timeout: 3000 })
      .eq(1)
      .click({ force: true })
    cy.get("[cy-data=ProjectEdit]", { timeout: 3000 })
      .eq(1)
      .click({ force: true })
    cy.get("[cy-data=ProjectName]", { timeout: 3000 })
      .clear()
      .type("项目" + timestamp.toString())
    cy.get("[cy-data=ProjectDescribe]", { timeout: 3000 })
      .clear()
      .type("项目描述edit")
    cy.get("[cy-data=ProjectOK]", { timeout: 3000 }).click()
  })
  it("delete", () => {
    cy.visit("#/main/project")
    cy.get("[cy-data=ProjectSetting]", { timeout: 3000 })
      .eq(-1)
      .click({ force: true })
    cy.get("[cy-data=ProjectDelete]", { timeout: 3000 })
      .eq(1)
      .click({ force: true })
    cy.contains("p", "删除成功")
  })

  it("list page", () => {
    cy.visit("#/main/project")
    cy.get("[cy-data=ProjectPagination] > ul.el-pager > li.number", {
      timeout: 3000,
    })
      .eq(1)
      .click() // 点击第2页
    cy.get("[cy-data=ProjectPagination] > button.btn-next", {
      timeout: 3000,
    }).click() // 点击下一页
  })
})
