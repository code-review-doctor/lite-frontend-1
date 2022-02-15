import helper from '../../helpers'
import fixtures from '../../fixtures'

describe('Application', () => {
  // it('login', () => {
  //   cy.login()
  // })

  context('newly created application', () => {
    let organisationId
    let userToken

    before(async () => {
      // Retrieve user token
      const authResponse = await helper.post(
        'gov-users/authenticate/',
        fixtures.authUser(Cypress.env('sso_user'))
      )
      userToken = await authResponse.token

      // Create organisation
      const organisationResponse = await helper.post(
        'organisations/',
        fixtures.organisation(),
        { 'GOV-USER-TOKEN': userToken },
      )
      organisationId = organisationResponse.id

      // Update organsation status to Active
      await helper.put(
        `organisations/${organisationId}/status/`,
        { status: 'active'},
        { 'GOV-USER-TOKEN': userToken },
      )

      // Add user to organisation
      await helper.post(
        `organisations/${organisationId}/users/`,
        fixtures.userToOrg(Cypress.env('sso_user')),
        { 'GOV-USER-TOKEN': userToken },
      )
      
      // Create an application
      const applicationResponse = await helper.post(
        'applications/',
        fixtures.applicaton,
        fixtures.exporterHeader(userToken, organisationId)
      )

      cy.pause()
    })

    beforeEach(() => {
      cy.visit('/')
    })

    it('should approve a case', () => {
      cy.visit('/application/')
    })
  })
})
