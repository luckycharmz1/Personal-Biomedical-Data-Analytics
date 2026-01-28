import React from "react"
import { Streamlit, withStreamlitConnection } from "streamlit-component-lib"

const MyComponent = () => {
  return <div>Hello, this is my custom component!</div>
}

export default withStreamlitConnection(MyComponent)
