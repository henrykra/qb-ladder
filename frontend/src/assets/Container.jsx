import React from 'react';

export default function Container({ content }) {
    return (
        <div
            className='bg-slate-600/65 size-30 border-3 rounded-xl border-gray-50 border-dashed inset-shadow-sm/20 shadow-md/20 flex items-center justify-center'
        >
            {content}
        </div>
    )
}