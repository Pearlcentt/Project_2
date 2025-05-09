import React, { useContext } from 'react';
import { ChatContext } from '../context/ChatContext';

const DocumentPanel = () => {
  const { retrievedDocs } = useContext(ChatContext);
  
  return (
    <div className="w-1/3 border-l bg-gray-50 overflow-y-auto p-4">
      <h3 className="font-semibold text-lg mb-3 text-blue-700">Reference Sources</h3>
      {retrievedDocs.length > 0 ? (
        <div className="space-y-3">
          {retrievedDocs.map((doc, index) => (
            <div 
              key={index}
              className="p-3 border rounded-md bg-white hover:bg-gray-100 transition"
            >
              <div className="flex justify-between items-center mb-2">
                <span className="font-medium text-blue-600">Source {index + 1}</span>
                <span className="text-xs text-gray-500">{doc.length} chars</span>
              </div>
              <p className="text-sm text-gray-700 whitespace-pre-wrap">
                {doc.length > 200 ? `${doc.substring(0, 200)}...` : doc}
              </p>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-gray-500">No sources retrieved yet.</p>
      )}
    </div>
  );
};

export default DocumentPanel;