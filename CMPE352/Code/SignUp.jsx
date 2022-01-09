import React, { Component } from 'react';
import axios from 'axios';
import {Grid, GridColumn, GridRow} from 'semantic-ui-react'
import "./styles.css";

export default class SignUp extends Component {

    render() {
      return (
        <form className="ui form" onSubmit={this.submit}> // this creates a React form.
           <Grid id="layout-grid"> // this creates a React Grid structure.
               <GridRow> // /* Grid Unit as Field and its name.
                  <GridColumn width={8}>
                      <label>Name</label>
                  </GridColumn>
                  <Grid.Column>
                      <input
                          disabled={this.state.disabled}
                          type='text'
                          placeholder='Name'
                          onChange={(event) => {
                            this.updateName(event.target.value)
                          }}
                          value={this.state.name}
                      />
                  </Grid.Column>
               </GridRow> // */
               <GridRow>
                 <GridColumn>
                   <label>Surname</label>
                 </GridColumn>
                 <GridColumn>
                   <input
                       disabled={this.state.disabled}
                       type='text'
                       placeholder='Surname'
                       onChange={(event) => {
                         this.updateSurname(event.target.value)
                       }}
                       value={this.state.surname}
                   />
                 </GridColumn>
               </GridRow>
             <GridRow>
               <GridColumn>
                 <label>Email</label>
               </GridColumn>
               <GridColumn>
                 <input
                     disabled={this.state.disabled}
                     type='email'
                     placeholder='Email'
                     onChange={(event) => {
                       this.updateEmail(event.target.value)
                     }}
                     value={this.state.email}
                 />
               </GridColumn>
             </GridRow>
             <GridRow>
               <GridRow>
                 <GridColumn>
                   <label>Password</label>
                 </GridColumn>
                 <GridColumn>
                   <input
                       disabled={this.state.disabled}
                       type='password'
                       placeholder='Password'
                       onChange={(event) => {
                         this.updatePassword(event.target.value)
                       }}
                       value={this.state.password}
                   />
                 </GridColumn>
               </GridRow>
             </GridRow>
             <GridRow>
               <GridColumn>
                 <label>Location</label>
               </GridColumn>
               <GridColumn>
                 <input
                     disabled={this.state.disabled}
                     type='text'
                     placeholder='Location'
                     onChange={(event) => {
                       this.updateLocation(event.target.value)
                     }}
                     value={this.state.location}
                 />
               </GridColumn>
             </GridRow>
             <GridRow>
               <button // Submit button.
                   disabled={this.state.disabled}
                   onClick={this.submit.bind(this)}>
                 Sign Up
               </button>
             </GridRow>
           </Grid>
        </form>
      )
  }
}