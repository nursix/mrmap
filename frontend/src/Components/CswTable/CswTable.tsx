import { Button, Space } from 'antd';
import React, { useRef } from 'react';
import CswRepo from '../../Repos/CswRepo';
import RepoTable, { RepoActionType, RepoTableColumnType } from '../Shared/RepoTable/RepoTable';
import { buildSearchTransformDateRange } from '../Shared/RepoTable/TableHelper';


const repo = new CswRepo();

const CswTable = (): JSX.Element => {
  const actionRef = useRef<RepoActionType>();
  const columns: RepoTableColumnType[] = [{
    dataIndex: 'id',
    title: 'ID'
  }, {
    dataIndex: 'title',
    title: 'Titel'
  }, {
    dataIndex: 'abstract',
    title: 'Zusammenfassung'
  }, {
    dataIndex: 'created_at',
    title: 'Erstellt',
    hideInSearch: true
  }, {
    dataIndex: 'created_between',
    title: 'Erstellt',
    valueType: 'dateRange',
    fieldProps: {
      format: 'DD.MM.YYYY',
      allowEmpty: [true, true]
    },
    search: {
      transform: buildSearchTransformDateRange('created_at')
    },
    hideInTable: true
  }, {
    dataIndex: 'last_modified_at',
    title: 'Modifiziert',
    hideInSearch: true
  }, {
    dataIndex: 'last_modified_between',
    title: 'Modifiziert',
    valueType: 'dateRange',
    fieldProps: {
      format: 'DD.MM.YYYY',
      allowEmpty: [true, true]
    },
    search: {
      transform: buildSearchTransformDateRange('last_modified_at')
    },
    hideInTable: true
  }, {
    dataIndex: 'version',
    title: 'Version'
  }, {
    dataIndex: 'service_url',
    title: 'Service URL'
  }, {
    dataIndex: 'get_capabilities_url',
    title: 'Capabilities URL'
  }, {
    dataIndex: 'xml_backup_file',
    hideInTable: true,
    hideInSearch: true
  }, {
    dataIndex: 'file_identifier',
    hideInTable: true,
    hideInSearch: true
  }, {
    dataIndex: 'access_constraints',
    hideInTable: true,
    hideInSearch: true
  }, {
    dataIndex: 'fees',
    hideInTable: true,
    hideInSearch: true
  }, {
    dataIndex: 'use_limitation',
    hideInTable: true,
    hideInSearch: true
  }, {
    dataIndex: 'license_source_note',
    hideInTable: true,
    hideInSearch: true
  }, {
    dataIndex: 'date_stamp',
    hideInTable: true,
    hideInSearch: true
  }, {
    dataIndex: 'origin',
    hideInTable: true,
    hideInSearch: true
  }, {
    dataIndex: 'origin_url',
    hideInTable: true,
    hideInSearch: true
  }, {
    dataIndex: 'is_broken',
    hideInTable: true,
    hideInSearch: true
  }, {
    dataIndex: 'is_customized',
    hideInTable: true,
    hideInSearch: true
  }, {
    dataIndex: 'insufficient_quality',
    hideInTable: true,
    hideInSearch: true
  }, {
    dataIndex: 'is_searchable',
    hideInTable: true,
    hideInSearch: true
  }, {
    dataIndex: 'hits',
    hideInTable: true,
    hideInSearch: true
  }, {
    dataIndex: 'is_active',
    hideInTable: true,
    hideInSearch: true
  }, {
    key: 'actions',
    title: 'Aktionen',
    valueType: 'option',
    render: (text: any, record:any) => {
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
          </Space>
        </>
      );
    }
  }];

  return <RepoTable
    repo={repo}
    columns={columns}
    actionRef={actionRef as any}
    onAddRecord='/registry/services/csw/add'
  />;
};

export default CswTable;
