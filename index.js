import React from 'react';
import { streamlitComponent } from 'streamlit-component-lib';

const MyComponent = () => {
    return <div>Hello, this is my custom component!</div>;
};

export default streamlitComponent(MyComponent);
