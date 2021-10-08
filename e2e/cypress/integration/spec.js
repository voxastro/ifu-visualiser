it('Trivial test /api', () => {
  cy.visit('/api')
})

it('Trivial test /api/cubes', () => {
  cy.visit('/api/cubes')
})

it('Check json format for /api/cubes', () => {
  cy.request('/api/cubes?format=json')
    .its('headers')
    .its('content-type')
    .should('include', 'application/json')
})

it('Check json format for /api/atlas_param', () => {
  cy.request('/api/atlas_param?format=json')
    .its('headers')
    .its('content-type')
    .should('include', 'application/json')
})

it('Check json format for /api/atlas_morphkin', () => {
  cy.request('/api/atlas_morphkin?format=json')
    .its('headers')
    .its('content-type')
    .should('include', 'application/json')
})

it('Check json format for /api/califa_object', () => {
  cy.request('/api/califa_object?format=json')
    .its('headers')
    .its('content-type')
    .should('include', 'application/json')
})

it('Check json format for /api/sami_cube_obs', () => {
  cy.request('/api/sami_cube_obs?format=json')
    .its('headers')
    .its('content-type')
    .should('include', 'application/json')
})
