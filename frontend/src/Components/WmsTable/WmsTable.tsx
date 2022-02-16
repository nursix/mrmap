import { LockOutlined, UnlockOutlined } from '@ant-design/icons';
import { Button, Space } from 'antd';
import React, { useRef } from 'react';
import { useNavigate } from 'react-router';
import RepoTable, { RepoActionType, RepoTableColumnType } from '../Shared/RepoTable/NewRepoTable';
import { buildSearchTransformDateRange } from '../Shared/RepoTable/TableHelper';


const WmsTable = (): JSX.Element => {
  const actionRef = useRef<RepoActionType>();
  const navigate = useNavigate();
  const columns: RepoTableColumnType[] = [{
    dataIndex: 'id',
  }, {
    dataIndex: 'title',
  }, {
    dataIndex: 'abstract',
  }, {
    dataIndex: 'createdAt',
    hideInSearch: true
  }, {
    dataIndex: 'createdBetween',
    valueType: 'dateRange',
    fieldProps: {
      format: 'DD.MM.YYYY',
      allowEmpty: [true, true]
    },
    search: {
      transform: buildSearchTransformDateRange('createdAt')
    },
    hideInTable: true
  }, {
    dataIndex: 'lastModifiedAt',
    hideInSearch: true
  }, {
    dataIndex: 'lastModifiedBetween',
    valueType: 'dateRange',
    fieldProps: {
      format: 'DD.MM.YYYY',
      allowEmpty: [true, true]
    },
    search: {
      transform: buildSearchTransformDateRange('lastModifiedAt')
    },
    hideInTable: true
  }, {
    dataIndex: 'version',
  }, {
    dataIndex: 'serviceUrl',
  }, {
    dataIndex: 'getCapabilitiesUrl',
  }, {
    dataIndex: 'xmlBackupFile',
    hideInTable: true,
    hideInSearch: true
  }, {
    dataIndex: 'fileIdentifier',
    hideInTable: true,
    hideInSearch: true
  }, {
    dataIndex: 'accessConstraints',
    hideInTable: true,
    hideInSearch: true
  }, {
    dataIndex: 'fees',
    hideInTable: true,
    hideInSearch: true
  }, {
    dataIndex: 'useLimitation',
    hideInTable: true,
    hideInSearch: true
  }, {
    dataIndex: 'licenseSourceNote',
    hideInTable: true,
    hideInSearch: true
  }, {
    dataIndex: 'dateStamp',
    hideInTable: true,
    hideInSearch: true
  }, {
    dataIndex: 'origin',
    hideInTable: true,
    hideInSearch: true
  }, {
    dataIndex: 'originUrl',
    hideInTable: true,
    hideInSearch: true
  }, {
    dataIndex: 'isBroken',
    hideInTable: true,
    hideInSearch: true
  }, {
    dataIndex: 'isCustomized',
    hideInTable: true,
    hideInSearch: true
  }, {
    dataIndex: 'insufficientQuality',
    hideInTable: true,
    hideInSearch: true
  }, {
    dataIndex: 'isSearchable',
    hideInTable: true,
    hideInSearch: true
  }, {
    dataIndex: 'hits',
    hideInTable: true,
    hideInSearch: true
  }, {
    dataIndex: 'isActive',
    hideInTable: true,
    hideInSearch: true
  }, {
    key: 'actions',
    title: 'Aktionen',
    valueType: 'option',
    render: (text: any, record:any) => {
      const isSecured = record.allowedOperations > 0;
      return (
        <>
          <Space size='middle'>
            <Button
              danger
              size='small'
              onClick={ () => {
                actionRef.current?.deleteRecord(record);
              }}
            >
              Löschen
            </Button>
            <Button
              size='small'
              icon={isSecured ? <LockOutlined/> : <UnlockOutlined/>}
              onClick={ () => {
                navigate(`/registry/services/wms/${record.id}/security`);
              }}
            >
              { isSecured ? `Zugriffsregeln: ${record.allowedOperations}` : 'Zugriff unbeschränkt' }
            </Button>
          </Space>
        </>
      );
    }
  }];

  return <RepoTable
    resourceType='WebMapService'
    columns={columns}
    actionRef={actionRef as any}
    onAddRecord='/registry/services/wms/add'
  />;
};

export default WmsTable;
