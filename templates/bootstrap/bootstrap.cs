using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using {$WORKERNAME!};
using Microsoft.Azure;

namespace Bootstrap
{
    class Program
    {
        static void Main(string[] args)
        {
            {$WORKERNAME!}.{$CLASSNAME!} x = new {$WORKERNAME!}.{$CLASSNAME!}();
            x.Run();
        }
    }
}
