import React from 'react';
import DatasetMetadataRepo from '../../Repos/DatasetMetadataRepo';
import RepoTable from '../Shared/Table/RepoTable';


const repo = new DatasetMetadataRepo();

const DatasetMetadataTable = (): JSX.Element => {
  return <RepoTable repo={repo} />;
};

export default DatasetMetadataTable;
