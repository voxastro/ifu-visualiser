describe('Basic API tests:', () => {
  it('Trivial test /api', () => {
    cy.visit(`${Cypress.env('backend')}/api`)
  })

  it('Trivial test /api/cubes/', () => {
    cy.visit(`${Cypress.env('backend')}/api/cubes?omit=spectrum`)
  })

  it('Check json format for /api/cubes/', () => {
    cy.request(`${Cypress.env('backend')}/api/cubes?format=json&omit=spectrum`)
      .its('headers')
      .its('content-type')
      .should('include', 'application/json')
  })

  it('Check json format for /api/atlas_param', () => {
    cy.request(`${Cypress.env('backend')}/api/atlas_param?format=json`)
      .its('headers')
      .its('content-type')
      .should('include', 'application/json')
  })

  it('Check json format for /api/atlas_morphkin', () => {
    cy.request(`${Cypress.env('backend')}/api/atlas_morphkin?format=json`)
      .its('headers')
      .its('content-type')
      .should('include', 'application/json')
  })

  it('Check json format for /api/califa_object', () => {
    cy.request(`${Cypress.env('backend')}/api/califa_object?format=json`)
      .its('headers')
      .its('content-type')
      .should('include', 'application/json')
  })

  it('Check json format for /api/sami_cube_obs', () => {
    cy.request(`${Cypress.env('backend')}/api/sami_cube_obs?format=json`)
      .its('headers')
      .its('content-type')
      .should('include', 'application/json')
  })

  it('Check json format for /api/manga_drp', () => {
    cy.request(`${Cypress.env('backend')}/api/manga_drp?format=json`)
      .its('headers')
      .its('content-type')
      .should('include', 'application/json')
  })
})

///////////////////////////////////////////////////////////////////////////////
describe('Search page', () => {
  it('focuses input on load', () => {
    cy.visit(`${Cypress.env('frontend')}/search`)
  })
})
