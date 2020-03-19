import React from 'react';
import { Spinner } from 'reactstrap';

function Loading(props) {
  return (
    <div>
      <Spinner color="primary" />
    </div>
  );
}

export default Loading;