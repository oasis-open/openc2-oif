import React, { Component } from 'react';
import { Dispatch } from 'redux';
import { ConnectedProps, connect } from 'react-redux';
import { Helmet } from 'react-helmet-async';
import DeviceModal from './modal';
import { ColumnDescriptionKeyed, RowEditOptions, RemotePageTable } from '../utils';
import { Device } from '../../actions';
import { RootState } from '../../reducers';

// Interfaces
// eslint-disable-next-line @typescript-eslint/no-empty-interface
interface DeviceProps {}

interface DeviceState {
  modal: boolean;
  device: Device.Device;
}

// Redux Connector
const mapStateToProps = (state: RootState) => ({
  siteTitle: state.Util.site_title,
  orchestrator: {
    name: state.Util.name || 'N/A'
  },
  admin: state.Auth.access?.admin || false
});

const mapDispatchToProps = (dispatch: Dispatch) => ({
  getDevices: (page: number, count: number, sort: string) => dispatch(Device.getDevices({page, count, sort})),
  deleteDevice: (dev: string) => dispatch(Device.deleteDevice(dev))
});

const connector = connect(mapStateToProps, mapDispatchToProps);
type ConnectorProps = ConnectedProps<typeof connector>;
type DeviceConnectedProps = DeviceProps & ConnectorProps;

// Component
class Devices extends Component<DeviceConnectedProps, DeviceState> {
  meta: {
    title: string;
    canonical: string;
  }

  tableColumns: Array<ColumnDescriptionKeyed>;
  editOptions: RowEditOptions;

  constructor(props: DeviceConnectedProps) {
    super(props);

    const { deleteDevice, siteTitle } = this.props;

    this.meta = {
      title: `${siteTitle} | Devices`,
      canonical: `${window.location.origin}${window.location.pathname}`
    };

    this.tableColumns = [
      {
        text: 'Name',
        dataField: 'name',
        sort: true
      }, {
        text: 'Transport',
        dataField: 'transport',
        formatter: (cell: Array<Device.Transport>) => ( <span>{ cell.map(t => `${t.serialization} via ${t.protocol}`).join(' | ') }</span> ),
        sort: true
      }
    ];

    this.editOptions = {
      modal: DeviceModal,
      delete: deleteDevice
    };
    // this.props.getDevices()
  }

  render() {
    const { admin, getDevices, orchestrator } = this.props;

    return (
      <div className="row mx-auto">
        <Helmet>
          <title>{ this.meta.title }</title>
          <link rel="canonical" href={ this.meta.canonical } />
        </Helmet>
        <div className="col-12">
          <div className="col-12">
            { admin ? <DeviceModal register className="float-right" /> : '' }
            <h1>{ `${orchestrator.name} Devices` }</h1>
          </div>

          <RemotePageTable
            keyField='device_id'
            dataKey='Device.devices'
            dataGet={ getDevices }
            columns={ this.tableColumns }
            editRows
            editOptions={ this.editOptions }
            defaultSort={
              [
                {
                  dataField: 'name',
                  order: 'desc'
                },
                {
                  dataField: 'transport',
                  order: 'desc'
                }
              ]
            }
          />
        </div>
      </div>
    );
  }
}

export default connector(Devices);
