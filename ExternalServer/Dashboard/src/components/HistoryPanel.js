import React from 'react';
import { ListGroup, ListGroupItem, ListGroupItemHeading, ListGroupItemText } from 'reactstrap';

const HistoryList = (props) => {
  let topItem = true
  const historyList = props.danceData.map(dance => {
    return (
      <div key={dance.date}>
        <ListGroupItem style={ (topItem && !props.firstReceived)? {} : {'backgroundColor': '#3a86ce'}} >
          <ListGroupItemHeading style={{fontSize: 'calc(7px + 1.2vw)'}}>
            Dance Move: {dance.danceMove}
          </ListGroupItemHeading>
          <ListGroupItemText style={{fontSize: 'calc(5px + 0.8vw)'}}>
            Timestamp: { new Date(dance.date).toLocaleString() }
          </ListGroupItemText>
          {
            topItem = (topItem)? !topItem : topItem
          }
        </ListGroupItem>
        <br />
      </div>
    )
  })

  return (
    <div className='ContainerScroll'>
      <ListGroup style={{'textAlign': 'center', 'paddingLeft': '15px', 'paddingRight': '15px'}}>
        {!!(historyList) ? historyList: 'No Data'}
      </ListGroup>
    </div>
    
  );
}

export default HistoryList