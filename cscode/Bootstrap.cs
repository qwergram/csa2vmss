using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using ContosoAdsWorker;

namespace Bootstrap
{
    class Program
    {
        static void Main(string[] args)
        {
            WorkerRole x = new WorkerRole();
            x.Run();
        }
    }
}
