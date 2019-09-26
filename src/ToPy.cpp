#include <iostream>
#include <string>
#include <vector>
#include <Python.h>
#include <numpy/arrayobject.h>
#include <numpy/npy_math.h>
#include "pom_solver.h"
#include "global.h"

Room* room;
Vector<ProbaView *> *proba_views = 0;
Vector<scalar_t> prior;
Vector<scalar_t> proba_presence;

char* result_format = "";
char* result_view_format = "";

static PyObject* ParseRect(PyObject* pLine)
{
    Py_ssize_t len_line = PyList_Size(pLine);
    
    PyObject *Item;
    Item = PyList_GetItem(pLine, 1);
    Item = PyLong_FromUnicodeObject(Item,10);
    long n_camera = PyLong_AsLong(Item);
    
    Item = PyList_GetItem(pLine, 2);
    Item = PyLong_FromUnicodeObject(Item,10);
    long n_position = PyLong_AsLong(Item);
    
    bool visible = true;
    if (len_line == 4) 
        visible = false;
    
    Rectangle *current = room->avatar(n_camera, n_position);
    if(visible == false) {
        current->visible = false;
        current->xmin = -1;
        current->ymin = -1;
        current->xmax = -1;
        current->ymax = -1;
    } else {
        current->visible = true;
        Item = PyList_GetItem(pLine, 3);
        Item = PyLong_FromUnicodeObject(Item,10);
        current->xmin = PyLong_AsLong(Item);
        
        Item = PyList_GetItem(pLine, 4);
        Item = PyLong_FromUnicodeObject(Item,10);
        current->ymin = PyLong_AsLong(Item);
        
        Item = PyList_GetItem(pLine, 5);
        Item = PyLong_FromUnicodeObject(Item,10);
        current->xmax = PyLong_AsLong(Item);
        
        Item = PyList_GetItem(pLine, 6);
        Item = PyLong_FromUnicodeObject(Item,10);
        current->ymax = PyLong_AsLong(Item);

        if(current->xmin < 0 || current->xmax >= room->view_width() ||
           current->ymin < 0 || current->ymax >= room->view_height()) {
          cerr << "RECTANGLE[" << n_position << "]:(" 
          << current->xmin << "," 
          << current->ymin << ","
          << current->xmax << ","
          << current->ymax << ")"
          << "out of bounds" << std::endl;
          Py_RETURN_FALSE;
        }
        //cout << "ParseRect:" << current->xmin << endl;
    }
    Py_RETURN_TRUE;
}

static PyObject* ParseRoom(PyObject* pLine)
{
    assert(PyList_Size(pLine) == 5);

    long view_width = -1, view_height = -1;
    long nb_positions = -1;
    long nb_cameras = -1;

    PyObject *Item = PyList_GetItem(pLine, 1);
    Item = PyLong_FromUnicodeObject(Item,10);
    view_width = PyLong_AsLong(Item);

    Item = PyList_GetItem(pLine, 2);
    Item = PyLong_FromUnicodeObject(Item,10);
    view_height = PyLong_AsLong(Item);

    Item = PyList_GetItem(pLine, 3);
    Item = PyLong_FromUnicodeObject(Item,10);
    nb_cameras = PyLong_AsLong(Item);
 
    Item = PyList_GetItem(pLine, 4);
    Item = PyLong_FromUnicodeObject(Item,10);    
    nb_positions = PyLong_AsLong(Item);

    room = new Room(view_width, view_height, nb_cameras, nb_positions);
    proba_views = new Vector<ProbaView *>(nb_cameras);
    for(int c = 0; c < proba_views->length(); c++)
      (*proba_views)[c] = new ProbaView(view_width, view_height);
    prior = Vector<scalar_t>(room->nb_positions());
    for(int i = 0; i < room->nb_positions(); i++)
        prior[i] = global_prior;
    proba_presence = Vector<scalar_t>(room->nb_positions());

    std::cout << "ParseRoom:" 
              << " " << view_width
              << " " << view_height
              << " " << nb_cameras
              << " " << nb_positions
              << std::endl;

    Py_RETURN_TRUE;
}

static PyObject* update_room(PyObject* self, PyObject* args)
{
  PyObject *pList;
  
  if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &pList)) {
    PyErr_SetString(PyExc_TypeError, "parameter must be a list.");
    Py_DECREF(pList);
    Py_RETURN_FALSE;
  }
  
  PyObject *pLine;
  PyObject *Item;
  PyObject* pStrObj;
  Py_ssize_t len_list = PyList_Size(pList);
  
  
  for (int i = 0; i < len_list; i++) {
    pLine = PyList_GetItem(pList, i);
    Item  = PyList_GetItem(pLine, 0);
    pStrObj = PyUnicode_AsUTF8String(Item); 
    char* FirstStr = PyBytes_AsString(pStrObj);
    //cout << "FirstStr: " << FirstStr << endl;
    if(strcmp(FirstStr,"RECTANGLE") == 0){
		  ParseRect(pLine);
	  } else if(strcmp(FirstStr,  "ROOM") == 0){
		  ParseRoom(pLine);
	  } else if(strcmp(FirstStr, "PROBA_IGNORED") == 0) {
	      Item = PyList_GetItem(pLine, 1);
	      Item = PyFloat_FromString(Item);
        global_proba_ignored =  PyFloat_AsDouble(Item);
        std::cout << "GLOBAL_PROBA_IGNORED:" << global_proba_ignored << std::endl;
    }else if(strcmp(FirstStr,  "RESULT_VIEW_FORMAT") == 0){
	      Item = PyList_GetItem(pLine, 1);
	      pStrObj = PyUnicode_AsUTF8String(Item); 
        result_view_format = PyBytes_AsString(pStrObj);    
        std::cout << "RESULT_VIEW_FORMAT" << result_view_format << std::endl;
	  } else if(strcmp(FirstStr,  "RESULT_FORMAT") == 0){
		    Item = PyList_GetItem(pLine, 1);
	      pStrObj = PyUnicode_AsUTF8String(Item); 
        result_format = PyBytes_AsString(pStrObj);
        std::cout << "RESULT_FORMAT:" << result_format << std::endl;
	  }
  }
  
  /*
  Py_DECREF(Item);
  Py_DECREF(pStrObj); 
  Py_DECREF(pList);
  Py_DECREF(pLine);
  */
  Py_RETURN_TRUE;
}

static PyObject* solve(PyObject* self, PyObject* args)
{
    int frame;
    if (!PyArg_ParseTuple(args, "i", &frame)) // Crash
        return NULL;

    TestWrapper(room, &prior, proba_views, &proba_presence, frame, result_format,result_view_format);
    
    PyObject* ret_list = PyList_New(room->nb_positions());
    for(int i = 0; i < room->nb_positions(); i++){
            PyList_SetItem(ret_list, i, PyFloat_FromDouble(proba_presence[i]));
    }
    
    return ret_list;
}


static PyObject* sendImg(PyObject* self, PyObject* args)
{
    PyObject *py_array = NULL;
    int cam;
    if (!PyArg_ParseTuple(args, "iO", &cam,&py_array)) // Crash
        return NULL;
        
    int typenum = NPY_DOUBLE;
    PyArray_Descr *descr;
    descr = PyArray_DescrFromType(typenum);
    npy_intp dims[3];
    double ***png;
    if (PyArray_AsCArray(&py_array, (void **)&png, dims, 3, descr) < 0) {
      PyErr_SetString(PyExc_TypeError, "error converting to c array");
      return NULL;
    }
    
    (*proba_views)[cam]->from_image(png);
    Py_RETURN_TRUE;
}

static PyObject* update_prior(PyObject* self, PyObject* args)
{
    //our data 
    double *data;

    PyObject *pyarray = NULL;
    if (!PyArg_ParseTuple(args, "O", &pyarray)) // Crash
        return NULL;
        
    PyArray_Descr *descr;
    descr = PyArray_DescrFromType(NPY_DOUBLE);
    npy_intp dims[1];

    if (PyArray_AsCArray(&pyarray, (void *)&data, dims, 1, descr) < 0) {
      PyErr_SetString(PyExc_TypeError, "error converting to c array");
      return NULL;
    }

    for (size_t i = 0;i < room->nb_positions(); ++i)
      prior[i] = data[i];
    Py_RETURN_TRUE;
}

static PyMethodDef PyMethods[] =
{
  {"update_room"          , update_room         , METH_VARARGS, "update_room" },
  {"solve"                , solve            , METH_VARARGS, "solve" },
  {"sendImg"              , sendImg            , METH_VARARGS, "sendImg" },
  {"update_prior"         , update_prior            , METH_VARARGS, "update_prior" },
  {NULL                 , NULL              , 0           , NULL                                           }
};

/* Python 3.x code */

static struct PyModuleDef module_parsepom =
{
  PyModuleDef_HEAD_INIT,
  "parsepom", /* name of module */
  NULL,     /* module documentation, may be NULL */
  -1,       /* size of per-interpreter state of the module,
               or -1 if the module keeps state in global variables. */
  PyMethods
};

PyMODINIT_FUNC
PyInit_parsepom(void)
{
  import_array();
  (void) PyModule_Create(&module_parsepom);
}
