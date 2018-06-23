class SelectDegree extends React.Component {
  constructor(props) {
    super();
    this.state = {selectValue:'Select Degree'};
    this.handleDegreeChange=this.handleDegreeChange.bind(this)
  }

  handleDegreeChange(e) {
    this.setState({
      selectValue: e.target.value
    })
    this.props.appHandleDegreeChange(e.target.value)
  }

  render() {
    return (
      <div>
        <select name="SelectDegree" placeholder="Degree" value={this.state.selectValue} onChange={this.handleDegreeChange}>
          <option defaultValue="Select Degree" disabled>Select Degree</option>
          <option value="Associates">Associates</option>
          <option value="Bechelor">Bachelor</option>
          <option value="College">College</option>
          <option value="Master">Master</option>
          <option value="Ph.D.">Ph.D.</option>
          <option value="PostDoc">PostDoc</option>
        </select>
      </div>
    );
  }
}

class School extends React.Component {
  constructor() {
    super();
    this.handleSchoolChange = this.handleSchoolChange.bind(this)
  }

  handleSchoolChange(e) {
    this.props.appHandleSchoolChange(e.target.value)
  }

  render() {
    return (
      <div>
        <input 
          type='text' 
          placeholder="Enter School"
          onChange={this.handleSchoolChange} />
       </div>
    );
  }
}

class From extends React.Component {
  constructor() {
    super();
    this.handleFromChange = this.handleFromChange.bind(this)
  }

  handleFromChange(e) {
    this.props.appHandleFromChange(e.target.value)
  }

  render() {
    return (
      <div float="left">
      <input type='date' placeholder={this.props.value} onChange={this.handleFromChange}/>
      </div>
    );
  }
}


class To extends React.Component {
  constructor() {
    super();
    this.handleToChange = this.handleToChange.bind(this)
  }

  handleToChange(e) {
    this.props.appHandleToChange(e.target.value)
  }

  render() {
    return (
      <div float="left">
      <input type='date' placeholder={this.props.value} onChange={this.handleToChange}/>
      </div>
    );
  }
}

class AddEducation extends React.Component {
  constructor() {
    super();
    this.handleClick = this.handleClick.bind(this)
  }
  
  handleClick() {
    this.props.handleClick()
  }

  render() {
    return (
      <div>
        <button type="button" onClick={this.handleClick}>Add</button>
      </div>
    )
  }
}

class RemoveLastEducation extends React.Component {
  constructor() {
    super();
    this.handleClick = this.handleClick.bind(this)
  }
  
  handleClick() {
    this.props.handleClick()
  }

  render() {
    return (
      <div>
        <button type="button" onClick={this.handleClick}>Remove Last Added Education</button>
      </div>
    )
  }
}

class Education extends React.Component {
  render() {
    return (
      <div>
        <h1 className="Education">{this.props.title}</h1>
        <SelectDegree appHandleDegreeChange={this.props.appHandleDegreeChange} />
        <School appHandleSchoolChange={this.props.appHandleSchoolChange}/>
        <From appHandleFromChange={this.props.appHandleFromChange}/>
        <To appHandleToChange={this.props.appHandleToChange}/>
        <AddEducation handleClick={this.props.appHandleAddEducation}/>
        <RemoveLastEducation handleClick={this.props.appHandleRemoveLastEducation}/>
      </div>
    )
  }
}

class Summary extends React.Component {
  render() {
    return (
      <div>
      <h1> Summary of Current Input </h1>
      <ul className="summary">
        {this.props.summary.Education.map(m => {
            return (
              <li k={m.id}>
                <div>
                  {m.Degree}
                </div>
                <div>
                  {m.School}
                </div>
                <div>
                  {m.From}
                </div>
                <div>
                  {m.To}
                </div>
              </li>
            )
          })}
       </ul>
       </div>
    )
  }
       //<p> {this.props.testMessage} </p>
}

const MockSummary = { 
  Education: [
    {
      Degree: "Master",
      School: "UC Berkeley",
      From: "2013-01-01",
      To: "2015-02-03"
    },
    {
      Degree: "Bechlor",
      School: "UC Berkeley",
      From: "2009-01-01",
      To: "2013-02-03"
    }
  ],
  Work: [
  ]
}

const EmptySummary = {Education:[],Work:[]}

class App extends React.Component {
  constructor() {
    super()
    this.state = {
      //summary: MockSummary,
      summary: EmptySummary,
      currentSelectedDegree: "",
      currentSchool:"",
      currentFrom:"",
      currentTo:"",
      result:"no response yet"
    }
    this.handleDegreeChange=this.handleDegreeChange.bind(this)
    this.handleSchoolChange=this.handleSchoolChange.bind(this)
    this.handleFromChange=this.handleFromChange.bind(this)
    this.handleToChange=this.handleToChange.bind(this)
    this.handleAddEducation=this.handleAddEducation.bind(this)
    this.handleRemoveLastEducation=this.handleRemoveLastEducation.bind(this)
    this.handleSubmit=this.handleSubmit.bind(this)
  }

  handleDegreeChange(m) {
    this.setState({
      currentSelectedDegree: m
    })
  }

  handleSchoolChange(m) {
    this.setState({
      currentSchool: m
    })
  }

  handleFromChange(m) {
    this.setState({
      currentFrom: m
    })
  }

  handleToChange(m) {
    this.setState({
      currentTo: m
    })
  }

  handleAddEducation() {
    const sum = this.state.summary
    sum.Education.push({
      Degree: this.state.currentSelectDegree,
      School: this.state.currentSchool,
      From: this.state.currentFrom,
      To: this.state.currentTo
    })
    this.setState({
      summary: sum
    })
    this.setState({
      currentSelectDegree: "",
      currentSchool: "",
      currentFrom: "",
      currentTo: ""
    })
  }

  handleRemoveLastEducation() {
    const sum = this.state.summary
    const last = sum.Education[sum.Education.length - 1]
    this.setState({
      currentSelectDegree: last.Degree,
      currentSchool: last.School,
      currentFrom: last.From,
      currentTo: last.to
    })
    sum.Education.splice(-1,1)
    this.setState({summary: sum })
  }

  handleSubmit() {
    axios.get('http://localhost:8000/mockResponse.html')
         .then(response => this.setState({result: response.data})) 
         //.then(response => console.log(response)) 
  }
  
  render() {
    return (
      <div className="app">
        <Summary summary={this.state.summary} testMessage={this.state.currentSelectedDegree +" " + this.state.currentSchool + " " + this.state.currentFrom + " " + this.state.currentTo}/>
        <Education title="Education" appHandleDegreeChange={this.handleDegreeChange} appHandleSchoolChange={this.handleSchoolChange} appHandleFromChange={this.handleFromChange} appHandleToChange={this.handleToChange} appHandleAddEducation={this.handleAddEducation} appHandleRemoveLastEducation={this.handleRemoveLastEducation} currentSummary = {this.state.summary.Education}/>
        <button type="button" onClick={this.handleSubmit}> Submit Education </button>
        <p>{this.state.result}</p>
      </div>
    )
  }
}


ReactDOM.render(
    <App />, 
    document.getElementById("root")
);
